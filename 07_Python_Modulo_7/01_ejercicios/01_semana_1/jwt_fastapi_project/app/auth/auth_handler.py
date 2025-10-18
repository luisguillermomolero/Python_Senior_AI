from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
import secrets
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración JWT desde variables de entorno
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Generar SECRET_KEY automáticamente con secrets si no existe
    SECRET_KEY = secrets.token_urlsafe(32)
    print(f"⚠️  ADVERTENCIA: SECRET_KEY no encontrada en .env")
    print(f"🔑 Usando clave temporal generada: {SECRET_KEY}")
    print(f"💡 Para producción, agrega esta clave a tu archivo .env")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def crear_token(data: dict, expiracion: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiracion)
    
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
