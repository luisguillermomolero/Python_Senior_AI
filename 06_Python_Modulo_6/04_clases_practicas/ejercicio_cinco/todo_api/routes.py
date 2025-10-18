from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import TareaBase, TareaCrear, TareaActualizar, TareaRespuesta
from data import tareas
import uuid

router = APIRouter()

@router.post("/tareas/")
async def crear_tarea(tarea: TareaCrear):
    tarea_id = str(uuid.uuid4())
    nueva_tarea = tarea.model_dump()
    tareas[tarea_id] = nueva_tarea
    
    return  JSONResponse(
        status_code=201,
        content={
            "exito": True,
            "mensaje": "Tarea Creada",
            "tarea": TareaRespuesta(id=tarea_id, **nueva_tarea).model_dump()
        }
    )

@router.get("/tareas/")
async def obtener_tareas():
    if not tareas:
        return JSONResponse(
            status_code=404,
            content={
                "exito":False,
                "mensaje":"No hay tareas registradas",
                "tareas":[]
            }
        )
    
    lista_tareas = [
        TareaRespuesta(id=tid, **data).model_dump()
        for tid, data in tareas.items()
    ]
    
    return JSONResponse(
        status_code=200,
        content={
            "exito":True,
            "tareas": lista_tareas
        }
    )

@router.get("/tareas/{tarea_id}")
async def obtener_tarea(tarea_id: str):
    if tarea_id not in tareas:
        return JSONResponse(
            status_code=404,
            content={
                "exito":False,
                "mensaje":"Tarea no encontrada"
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "exito":True,
            "tarea": TareaRespuesta(id=tarea_id, **tareas[tarea_id]).model_dump()
        }
    )

@router.put("/tareas/{tarea_id}")
async def actualizar_tarea(tarea_id: str, tarea_actualizar: TareaActualizar):
    if tarea_id not in tareas:
        return JSONResponse(
            status_code=404,
            content={
                "exito":False,
                "mensaje":"Tarea no encontrada"
            }
        )
    
    tarea_existente = tareas[tarea_id]
    datos_actualizados = tarea_actualizar.model_dump(exclude_unset=True)
    tarea_existente.update(datos_actualizados)
    tareas[tarea_id] = tarea_existente
    
    return JSONResponse(
        status_code=200,
        content={
            "exito":True,
            "mensaje": f"La tarea con ID {tarea_id} fue actualizada exitosamente",
            "tarea": TareaRespuesta(id=tarea_id, **tarea_existente).model_dump()
        }
    )

@router.delete("/tareas/{tarea_id}")
async def eliminar_tarea(tarea_id: str):
    if tarea_id not in tareas:
        return JSONResponse(
            status_code=404,
            content={
                "exito":False,
                "mensaje":"Tarea no encontrada"
            }
        )
    
    tarea_eliminada = tareas.pop(tarea_id)
    
    return JSONResponse(
        status_code=200,
        content={
            "exito":True,
            "mensaje":f"La tarea con el ID {tarea_id} ha sido eliminada satisfactoriamente",
            "tarea":TareaRespuesta(id=tarea_id, **tarea_eliminada).model_dump()
        }
    )

