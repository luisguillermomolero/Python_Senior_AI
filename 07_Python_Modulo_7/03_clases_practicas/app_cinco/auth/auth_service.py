from passlib.context import CryptContext

HASH_SCHEMA = "argon2"

pwd_context = CryptContext(schemes=[HASH_SCHEMA], deprecated="auto")

def hashear_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


