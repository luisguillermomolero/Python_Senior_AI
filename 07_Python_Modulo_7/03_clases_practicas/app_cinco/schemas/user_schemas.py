from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único", examples=["juan_perez"]) 
    password: str = Field(..., min_length=6, description="Contraseña el usuario", examples=["Micontrasena123"])
    
class UserLogin(BaseModel):
    username: str = Field(..., description="Nombre de usuario", examples=["juan_perez"])
    password: str = Field(..., description="Contraseña de usuario", examples=["Micontrasena123"])

class UserResponse(BaseModel):
    id: int = Field(examples=[1])
    username: str = Field(examples=["juan_perez"])
    created_at: Optional[datetime] = Field(default=None, examples=["2025-10-09T14:30:00"])
    updated_at: Optional[datetime] = Field(default=None, examples=[None])
    
    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token: str = Field(..., description="Token JWT de acceso", examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(default="bearer", description="Tipo de token", examples=["bearer"])

class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT de acceso", examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(default="bearer", description="Tipo de token", examples=["bearer"])
    user: UserResponse = Field(..., description="Datos de usuario autenticado")

class Message(BaseModel):
    mensaje: str = Field(examples=["Operación realizada exitosamente"])


