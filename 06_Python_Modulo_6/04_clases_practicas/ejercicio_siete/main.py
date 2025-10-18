from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date
import uuid
from sqlalchemy import Column, String, Float, Date, Text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from config import engine, Base, get_db

# Modelo de pydantic
# Proyecto

class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, examples="Sistema de Gestión de proyectos web")
    descripcion: str = Field(..., min_length=10, max_length=500, examples="Desarrollo de una app para gestion de proyectos web")
    presupuesto: float = Field(..., gt=0, le=10000000, examples=2500.33)
    fecha_inicio: str = Field(..., description="YYYY-MM-DD", examples="2025-09-25")
    estado: str = Field(..., pattern=r"^(planificacion|en_progreso|completado|cancelado)$", example="planificación")

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100, examples="Actualización del nombre")
    descripcion: Optional[str] = Field(None, min_length=10, max_length=500, examples="Actualización de la descripción")
    presupuesto: Optional[float] = Field(None, gt=0, le=10000000, examples=123456.45)
    fecha_inicio: Optional[str] = Field(None, description="YYYY-MM-DD", examples="2020-10-10")
    estado: Optional[str] = Field(None, pattern=r"^(planificacion|en_progreso|completado|cancelado)$", example="en_progreso")

class ProyectoResponse(ProyectoBase):
    proyecto_id: str = Field(..., description="ID único generado por uuid", examples="550e8400-e29b-41d4-a716-446655440000")

# Cliente

class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, examples="Luis Guillermo Molero Suárez")
    email: EmailStr = Field(..., examples="luisguillermomolero.suarez@gmail.com")
    telefono: str = Field(..., min_length=7, max_length=20, examples="+573254568920")
    empresa: str =  Field(..., min_length=2, max_length=100, examples="Soluciones Tecnológicas S.A.S")
    direccion: str = Field(..., min_length=10, max_length=200, examples="Calle 55 #45-67 Manizales, Colombia")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50, examples="Actualización del nombre")
    email: Optional[EmailStr] = Field(None, examples="Actualización del correo")
    telefono: Optional[str] = Field(None, min_length=7, max_length=20, examples="+571231231212")
    empresa: Optional[str] =  Field(None, min_length=2, max_length=100, examples="Actualización de la empresa")
    direccion: Optional[str] = Field(None, min_length=10, max_length=200, examples="Actualización de la direccion")

class ClienteResponse(ClienteBase):
    cliente_id: str = Field(..., description="ID único generado por uuid", examples="550e8400-e29b-41d4-a716-446655440000")
    

# Modelos ORM

# Proyectos

class Proyecto(Base):
    __tablename__ = "proyectos"
    __table_args__ = {'extend_existing': True}
    
    proyecto_id = Column(String(36), primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    presupuesto = Column(Float, nullable=False)
    fecha_inicio = Column(Date, nullable=False)

# Clientes

class Cliente(Base):
    __tablename__ = "clientes"
    __table_args__ = {'extend_existing': True}
    
    cliente_id = Column(String(36), primary_key=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=False)
    empresa = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    
# Routers personalizados

proyectos_router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"],
    responses={404:{"descripcion":"Proyecto no encontrado"}}
)

clientes_router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
    responses={404:{"descripcion":"Proyecto no encontrado"}}
)

# API de Productos

@proyectos_router.post(
    "/",
    response_model=ProyectoResponse,
    status_code=status.HTTP_201_CREATE,
    summary="Crear un nuevo proyecto"
)
async def crear_proyecto(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    try:
        proyecto_id = str(uuid.uuid4())
        fecha_dt = date.fromisoformat(proyecto.fecha_inicio)
        orm_obj = Proyecto(
            proyecto_id=proyecto_id,
            nombre=proyecto.nombre,
            descripcion=proyecto.descripcion,
            presupuesto=float(round(proyecto.presupuesto, 2)),
            fecha_inicio=fecha_dt,
            estado=proyecto.estado
        )
        
        db.add(orm_obj)
        db.commit()
        db.refresh(orm_obj)
        return{
            "proyecto_id": orm_obj.proyecto_id,
            "nombre": orm_obj.nombre,
            "descripcion": orm_obj.descripcion,
            "presupuesto": orm_obj.presupuesto,
            "fecha_inicio": orm_obj.fecha_inicio.strftime("%Y-%m-%d"),
            "estado": orm_obj.estado,
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@proyectos_router.get(
    "/",
    response_model=List[ProyectoResponse],
    summary="Obtener todos los proyectos"
)
async def get_all_proyectos(db: Session = Depends(get_db)):
    try:
        rows = db.query(Proyecto).all()
        return[
            {
                "proyecto_id": r.proyecto_id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "presupuesto": r.presupuesto,
                "fecha_inicio": r.fecha_inicio.strftime("%Y-%m-%d"),
                "estado": r.estado,
            }
            for r in rows
        ]
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@proyectos_router.get(
    "/{proyecto_id}",
    response_model=ProyectoResponse,
    summary="Obtener un proyecto por ID"
)
async def read_proyecto(proyecto_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(proyecto_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Formato de ID de proyecto inválido. Debe ser un UUID válido...")
    
    try:
        obj = db.query(Proyecto).filter(Proyecto.proyecto_id == proyecto_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        return{
            "proyecto_id": obj.proyecto_id,
            "nombre": obj.nombre,
            "descripcion": obj.descripcion,
            "presupuesto": obj.presupuesto,
            "fecha_inicio": obj.fecha_inicio.strftime("%Y-%m-%d"),
            "estado": obj.estado,
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@proyectos_router.put(
    "/{proyecto_id}",
    response_model=ProyectoResponse,
    summary="Actualizar un proyecto existente"
)
async def update_proyecto(proyecto_id: str, proyecto = ProyectoUpdate, db: Session = Depends(get_db)):
    try:
        uuid.UUID(proyecto_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Formato de ID de proyecto inválido. Debe ser un UUID válido...")
    
    try:
        obj = db.query(Proyecto).filter(Proyecto.proyecto_id == proyecto_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        data = proyecto.model_dump(exclude_unset=True)
        if "fecha_inicio" in data and data["fecha_inicio"] is not None:
            data["fecha_inicio"] = date.fromisoformat(data["fecha_inicio"])
        for k, v in data.items()():
            setattr(obj, k, v)
        
        db.commit()
        db.refresh(obj)
        return{
            "proyecto_id": obj.proyecto_id,
            "nombre": obj.nombre,
            "descripcion": obj.descripcion,
            "presupuesto": obj.presupuesto,
            "fecha_inicio": obj.fecha_inicio.strftime("%Y-%m-%d"),
            "estado": obj.estado,
        }
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@proyectos_router.delete(
    "/{proyecto_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un proyecto existente"
)
async def delete_proyecto(proyecto_id: str, db: Session = Depends(get_db)):
    try:
        uuid.UUID(proyecto_id)
    except ValueError:
        raise HTTPException(status_code=422, detail="Formato de ID de proyecto inválido. Debe ser un UUID válido...")
    
    try:
        obj = db.query(Proyecto).filter(Proyecto.proyecto_id == proyecto_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
        db.delete(obj)
        db.commit()
        return {"mensaje": "Proyecto eliminado con éxitos"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")