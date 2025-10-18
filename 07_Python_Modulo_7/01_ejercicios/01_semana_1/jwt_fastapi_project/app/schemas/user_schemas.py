# app/schemas/user_schemas.py

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# ------------------------------------------------------------
# Schema para crear un nuevo usuario (registro)
class UserCreate(BaseModel):
    """Schema para el registro de nuevos usuarios"""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único", examples=["juan_perez"])
    password: str = Field(..., min_length=6, description="Contraseña del usuario", examples=["miPassword123"])

# ------------------------------------------------------------
# Schema para login de usuario
class UserLogin(BaseModel):
    """Schema para autenticación de usuarios"""
    username: str = Field(..., description="Nombre de usuario", examples=["juan_perez"])
    password: str = Field(..., description="Contraseña del usuario", examples=["miPassword123"])

# ------------------------------------------------------------
# Schema para la respuesta de usuario (sin contraseña)
class UserResponse(BaseModel):
    """Schema para la respuesta de datos de usuario"""
    id: int = Field(examples=[1])
    username: str = Field(examples=["juan_perez"])
    created_at: Optional[datetime] = Field(default=None, examples=["2025-10-09T14:30:00"])
    updated_at: Optional[datetime] = Field(default=None, examples=[None])
    
    model_config = ConfigDict(from_attributes=True)  # Permite crear desde modelos ORM

# ------------------------------------------------------------
# Schema para la respuesta del token de autenticación
class Token(BaseModel):
    """Schema para la respuesta de autenticación JWT"""
    access_token: str = Field(..., description="Token JWT de acceso", examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(default="bearer", description="Tipo de token", examples=["bearer"])

# ------------------------------------------------------------
# Schema para la respuesta completa de login (token + usuario)
class LoginResponse(BaseModel):
    """Schema para la respuesta de login con token y datos del usuario"""
    access_token: str = Field(..., description="Token JWT de acceso", examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str = Field(default="bearer", description="Tipo de token", examples=["bearer"])
    user: UserResponse = Field(..., description="Datos del usuario autenticado")

# ------------------------------------------------------------
# Schema para mensajes generales
class Message(BaseModel):
    """Schema para mensajes de respuesta"""
    mensaje: str = Field(examples=["Operación realizada exitosamente"])

