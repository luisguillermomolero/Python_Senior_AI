from fastapi import FastAPI, HTTPException, Header
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
import secrets

HASH_SCHEME = "argon2"
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class RegistroData(BaseModel):
    username: str = Field(examples=["usuario1"])
    password: str = Field(examples=["miSuperClase123456"])
    
class LoginData(BaseModel):
    username: str = Field(examples=["usuario1"])
    password: str = Field(examples=["miSuperClase123456"])

app = FastAPI()

# Contexto de passlib - Instancia (contraseña)
pwd_context = CryptContext(schemes=[HASH_SCHEME], deprecated="auto")

# db 
usuarios = {}

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def crear_token(data: dict, expiration: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiration)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

@app.get("/")
async def root():
    return {"mensaje": "API de autenticación JWT"}

@app.post("/registro")
async def registrar_usuario(datos: RegistroData):
    if datos.username in usuarios:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    usuarios[datos.username] = hashear_password(datos.password)
    
    return{
        "success": True,
        "mensaje": "Usuario registrado exitosamente",
        "usuario": {
            "username": datos.username,
            "password": datos.password,
            "registrado_en": datetime.now(timezone.utc).isoformat()
        }
    }
        
@app.post("/login")
async def login(datos: LoginData):
    user_pass = usuarios.get(datos.username)
    if not user_pass or not verificar_password(datos.password, user_pass):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = crear_token({"sub": datos.username})
    
    return{
        "success": True,
        "mensaje": "Login exitoso",
        "access_token": token,
        "expire_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "usuario":{
            "username": datos.username,
            "Hash_de_retorno": user_pass
        }
    }

def main():
    import uvicorn
    import webbrowser
    import threading
    
    def abrir_navegador():
        import time
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000/docs")
    
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
