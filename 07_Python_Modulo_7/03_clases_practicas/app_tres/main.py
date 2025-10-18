from passlib.context import CryptContext

HASH_SCHEME = "argon2"

pwd_context = CryptContext(schemes=[HASH_SCHEME], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain_password: str, hashed_password: str):
    password_verify = pwd_context.verify(plain_password, hashed_password)
    
    if not password_verify:
        raise ValueError("Contraseña incorrecta")

def main():
    print("Registro de usuario")
    registro_password = input("Introduzca una contraseña para registrarse: ")
    hashed = hash_password(registro_password)
    print(f"Hash generado: {hashed}")
    
    try:
        verificar_password(registro_password, hashed)
        print("Contraseña correcta")
    except ValueError as e:
        print(f"Error {e}")

if __name__ == "__main__":
    main()