from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# Modelos para las API los recursos
class RecursoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del recurso", examples=["Mi recurso"])
    descripción: Optional[str] = Field(None, max_length=200, description="Descripción opcional del recurso", examples=["Esta es una descripción del recurso"])
    
# Modelo para crear un recurso (entrada)
class RecursoCreate(RecursoBase):
    pass

# Modelo para actualizar recursos
class RecursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=50, examples=["Recurso actualizado"])
    descripcion: Optional[str] = Field(None, max_length=200, examples=["Nueva descripción"])

# Modelo para respuestas
class RecursoResponse(RecursoBase):
    item_id: int = Field(..., gt=0, description="ID único del recurso")

# Modelos para las API de usuario

class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=4, max_length=16, description="Nombre de usuario", examples=["luisitoComunica63"])
    email: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Correo electrónico válido",
        examples=["luistocomunica63@hotmail.com"]
    )
    edad: int = Field(..., gt=0, lt=120, description="Edad entre 1 y 119", examples=["25"])
    
class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=4, max_length=16, examples=["Actualización de usuario"])
    email: Optional[str] = Field(
        None,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["Actualización de email, ejemplo: luistocomunica63@hotmail.com"]
    )
    edad: Optional[int] = Field(None, gt=0, lt=120, examples=["25"])

class UsuarioResponse(UsuarioBase):
    user_id: int = Field(..., gt=0, description="ID único del usuario")


db_recursos: List[Dict] = []
next_recurso_id = 1

db_usuarios: List[Dict] = []
next_usuario_id = 1

recurso_router = APIRouter(
    prefix="/recursos",
    tags=["Recursos"],
    responses={
        404: {"descripción": "Recurso no encontrado"}
    }
)

usuarios_router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    responses={
        404: {"descripción": "Usuario no encontrado"}
    }
)

# Endpoint de recursos (APIResp)

@recurso_router.post(
    "/",
    response_model=RecursoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo Recurso"
)
async def create_recurso(recurso: RecursoCreate):
    global next_recurso_id
    new_item = recurso.model_dump()
    new_item["item_id"] = next_recurso_id
    db_recursos.append(new_item)
    next_recurso_id += 1
    return new_item

@recurso_router.get(
    "/",
    response_model=List[RecursoResponse],
    summary="Obtener todos los Recursos"
)
async def get_all_recursos():
    return db_recursos

@recurso_router.get(
    "/{item_id}",
    response_model=RecursoResponse,
    summary="Obtener un Recurso por ID"
)
async def read_recurso(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=422, detail="ID de Recuros inválido")
    for item in db_recursos:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Recurso no encontrado")

@recurso_router.put(
    "/{item_id}",
    response_model=RecursoResponse,
    summary="Actualizar un Recurso existente"
)
async def update_recurso(item_id: int, recurso: RecursoUpdate):
    if item_id <= 0:
        raise HTTPException(status_code=422, detail="ID de Recuros inválido")
    for item in db_recursos:
        if item["item_id"] == item_id:
            update_data = recurso.model_dump(exclude_unset=True)
            item.update(update_data)
            return item
    raise HTTPException(status_code=404, detail="Recurso no encontrado")

@recurso_router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un Recurso"
)
async def delete_recurso(item_id: int):
    global db_recursos
    if item_id <= 0:
        raise HTTPException(status_code=422, detail="ID de Recuros inválido")
    for item in db_recursos:
        if item["item_id"] == item_id:
            db_recursos.remove(item)
            return {
                "mensaje": "Recurso eliminado con éxito"
            }
    raise HTTPException(status_code=404, detail="Recurso no encontrado")

# Endpoint de Usuarios (APIRest)

@usuarios_router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo Usuario"
)
async def create_usuario(usuario: UsuarioCreate):
    global next_usuario_id
    new_user = usuario.model_dump()
    new_user["user_id"] = next_usuario_id
    db_usuarios.append(new_user)
    next_usuario_id += 1
    return new_user

@usuarios_router.get(
    "/",
    response_model=List[UsuarioResponse],
    summary="Obtener todos los Usuarios"
)
async def get_all_usuarios():
    return db_usuarios

@usuarios_router.get(
    "/{user_id}",
    response_model=UsuarioResponse,
    summary="Obtener un Usuario por ID"
)
async def read_usuario(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=422, detail="ID de Usuario inválido")
    for user in db_usuarios:
        if user["user_id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@usuarios_router.put(
    "/{user_id}",
    response_model=UsuarioResponse,
    summary="Actualizar un Usuario existente"
)
async def update_usuario(user_id: int, usuario: UsuarioUpdate):
    if user_id <= 0:
        raise HTTPException(status_code=422, detail="ID de Usuario inválido")
    for user in db_usuarios:
        if user["user_id"] == user_id:
            updata_data = usuario.model_dump(exclude_unset=True)
            user.update(updata_data)
            return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@usuarios_router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un Usuario"
)
async def delete_usuario(user_id: int):
    global db_usuarios
    if user_id <= 0:
        raise HTTPException(status_code=422, detail="ID de Usuario inválido")
    for user in db_usuarios:
        if user["user_id"] == user_id:
            db_usuarios.remove(user)
            return {
                "mensaje": "Usuario eliminado con éxito"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

app = FastAPI(
    title="API de Recursos y Usuarios",
    description="Ejemplo de APIRest con FastAPI, APIRouter personalizados, validación con Pydantic y DB en memoria",
    version="1.0.0"
)

@app.get(
    "/",
    summary="Página (Layout) principal de la aplicación de APIRest"
)
async def root():
    return{
        "mensaje": "Bienvenido al sistema de Backend APIRest de Recursos y Usuarios",
        "versión": "1.0.0",
        "documentación":"/docs",
        "endpoints_personalizados": {
            "recursos": "/recursos",
            "usuarios": "/usuarios"
        }
    }

app.include_router(recurso_router)
app.include_router(usuarios_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
    