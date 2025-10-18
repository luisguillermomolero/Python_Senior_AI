from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

articulos: Dict[int, dict]  = {}

class ArticuloBase(BaseModel):
    nombre: str
    descripcion: str | None = None # ALT 124
    precio: float
    impuesto: float | None = None

class ArticuloCrear(ArticuloBase):
    pass

class ArticuloActualizar(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    impuesto: float | None = None

class ArticuloRespuesta(ArticuloBase):
    id: int

@app.get("/")
def raiz():
    return JSONResponse(
        status_code=200,
        content={"exito": True, 
                 "mensaje": "Bienvenido a la API de articulos"
                 }
        )

@app.get("/articulos", response_model=List[ArticuloRespuesta])
def obtener_todos_articulos():
    if not articulos:
        return JSONResponse(
            status_code=404,
            content={"exito": False, 
                     "mensaje": "No se encontraron articulos", 
                     "articulos": []
                     }
            )
    
    lista_articulos = [ArticuloRespuesta(id=articulo_id, **datos).model_dump() for articulo_id, datos in articulos.items()]
    
    return JSONResponse(
        status_code=200,
        content={"exito": True, 
                 "articulos": lista_articulos
                 }
        )

@app.get("/articulos/{articulo_id}", response_model=ArticuloRespuesta)
def obtener_articulo(articulo_id: int):
    if articulo_id not in articulos:
        return JSONResponse(
            status_code=404,
            content={"exito": False, 
                     "mensaje": "Articulo no encontrado"
                     }
            )

    return JSONResponse(
        status_code=200,
        content={"exitos": True, 
                 "articulo": ArticuloRespuesta(id=articulo_id, **articulos[articulo_id]).model_dump()}
        )

@app.post("/articulos/", response_model=ArticuloRespuesta)
def crear_articulo(articulo: ArticuloCrear):
    articulo_id = len(articulos) + 1
    articulos[articulo_id] = articulo.model_dump()
    return JSONResponse(
        status_code=201,
        content={
            "exito": True,
            "mensaje": "Articulo creado",
            "articulo": ArticuloRespuesta(id=articulo_id, **articulos[articulo_id]).model_dump()}
        )

@app.put("/articulos/{articulo_id}", response_model=ArticuloRespuesta)
def actualizar_articulo(articulo_id: int, articulo: ArticuloActualizar):
    if articulo_id not in articulos:
        return JSONResponse(
            status_code=404,
            content={
                "exitos": False,
                "mensaje": "Articulo no encontrado"
                }
            )
    
    articulo_guardado = articulos[articulo_id]
    datos_actualizados = articulo.model_dump(exclude_unset=True)
    articulo_guardado.update(datos_actualizados)
    articulos[articulo_id] = articulo_guardado
    
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "mensaje": "Articulo actualizado",
            "articulo": ArticuloRespuesta(id=articulo_id, **articulo_guardado).model_dump()
            }
        )

@app.delete("/articulos/{articulo_id}", response_model=ArticuloRespuesta)
def eliminar_articulo(articulo_id: int):
    if articulo_id not in articulos:
        return JSONResponse(
            status_code=404,
            content={"exito": False,
                     "mensaje": "Articulo no encontrado"}
            )
    
    articulo_eliminado = articulos.pop(articulo_id)
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "mensaje": f"El articulo con ID {articulo_id} fue eliminado exitosamente",
            "articulo": ArticuloRespuesta(id=articulo_id, **articulo_eliminado). model_dump()
        }
    )
    