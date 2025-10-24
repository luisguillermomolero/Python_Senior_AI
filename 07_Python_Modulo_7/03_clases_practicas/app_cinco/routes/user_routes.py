from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.user import User
from auth.auth_service import hashear_password, verificar_password
from auth.auth_handler import crear_token
from auth.dependencies import get_current_user
from schemas.user_schemas import UserCreate, UserLogin, UserResponse, Token, LoginResponse, Message

router = APIRouter(tags=["Autenticación"])

@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user or not verificar_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = crear_token({"sub": user.username})
    
    return LoginResponse(
        access_token=token,
        token_type= "bearer",
        user=UserResponse.model_validate(user)
    )
    
@router.post("/register", response_model=UserResponse, status_code=201, summary="Registrar nuevo usuario")
def register(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    
    if user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    hashed = hashear_password(data.password)
    
    nuevo_usuario = User(username=data.username, hashed_password=hashed)
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario

@router.get("me", response_model=UserResponse, summary="Obtener usuario actual")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

