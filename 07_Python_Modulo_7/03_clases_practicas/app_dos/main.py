from jose import jwt
from datetime import datetime, timedelta, timezone
import secrets

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TIME_EXPIRE = 30

def crear_token(datos: dict, expiration: int = ACCESS_TIME_EXPIRE):
    
    to_encode = datos.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiration)
    
    to_encode.update(
        {
            "exp": expire
        }
    )
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("Error: El token ha expirado")
        return None
    except jwt.JWTError:
        print("Error: Token inválido")
        return None

def main():
    datos_usuario = {
        "sub": "usuario123",
        "rol": "admin"
    }
    
    token_generado = crear_token(datos_usuario)
    
    print("\nToken JWT generado:\n")
    print(token_generado + "\n")
    
    print("Verificando el token...")
    datos_decodificados = verificar_token(token_generado)
    
    if datos_decodificados:
        print("\nToken válido")
        print("\nInformación:")
        print(datos_decodificados)
        
if __name__ == "__main__":
    main()
    