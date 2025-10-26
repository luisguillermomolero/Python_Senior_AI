from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.user_model import User
from auth.auth_service import hashear_password, verificar_password
from auth.auth_handler import crear_token
from auth.dependencies import get_current_user
from schemas.user_schemas import UserCreate, UserLogin, UserResponse, Token, LoginResponse, Message

router = APIRouter(tags=["Autenticación"])  # Tag para documentación Swagger

@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Autentica un usuario y devuelve un token JWT junto con los datos del usuario.
    
    - **username**: Nombre de usuario
    - **password**: Contraseña del usuario
    
    Retorna:
    - **access_token**: Token JWT para autenticación
    - **token_type**: Tipo de token (bearer)
    - **user**: Datos del usuario autenticado
    """
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user or not verificar_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = crear_token({"sub": user.username})
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )

@router.post("/register", response_model=UserResponse, status_code=201, summary="Registrar nuevo usuario")
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema.
    
    - **username**: Nombre de usuario único (mínimo 3 caracteres)
    - **password**: Contraseña (mínimo 6 caracteres)
    """
    user = db.query(User).filter(User.username == data.username).first()
    
    if user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed = hashear_password(data.password)

    nuevo_usuario = User(username=data.username, hashed_password=hashed, role=data.role)

    db.add(nuevo_usuario)
    db.commit()  # Confirmamos los cambios en la base de datos
    db.refresh(nuevo_usuario)  # Obtenemos la versión actualizada del usuario

    return UserResponse.model_validate(nuevo_usuario)

@router.get("/me", response_model=UserResponse, summary="Obtener usuario actual")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Obtiene los datos del usuario autenticado actualmente.
    
    Requiere autenticación mediante token JWT en el header:
    Authorization: Bearer <token>
    
    Retorna:
    - **id**: ID del usuario
    - **username**: Nombre de usuario
    - **is_active**: Estado del usuario
    - **created_at**: Fecha de creación
    - **updated_at**: Fecha de última actualización
    """
    return UserResponse.model_validate(current_user)

@router.get("/admin", summary="Ruta de administrador")
async def admin_route(current_user: User = Depends(get_current_user)):
    """
    Ruta protegida solo para administradores.
    
    Requiere autenticación mediante token JWT y rol de administrador.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden acceder a esta ruta")
    
    return {"message": f"Bienvenido, administrador {current_user.username}"}
