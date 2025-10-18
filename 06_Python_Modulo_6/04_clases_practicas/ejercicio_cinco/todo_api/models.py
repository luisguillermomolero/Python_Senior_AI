from pydantic import BaseModel
from typing import Optional, Literal

class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: Literal["pendiente", "en_progreso", "completada"] = "pendiente"

class TareaCrear(TareaBase):
    pass

class TareaActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Literal["pendiente", "en_progreso", "completada"] = None

class TareaRespuesta(TareaBase):
    id: str
