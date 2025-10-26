from passlib.context import CryptContext

# Contexto de encriptación y base de datos de usuarios
HASH_SCHEME = "argon2"

pwd_context = CryptContext(schemes=[HASH_SCHEME], deprecated="auto")

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
