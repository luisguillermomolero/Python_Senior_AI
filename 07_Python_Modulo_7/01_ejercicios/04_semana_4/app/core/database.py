from sqlalchemy import create_engine  # Permite crear el motor de conexión a la base de datos
from sqlalchemy.ext.declarative import declarative_base  # Permite definir clases ORM que se traducen a tablas
from sqlalchemy.orm import sessionmaker  # Permite crear sesiones para interactuar con la base de datos
from sqlalchemy.exc import SQLAlchemyError  # Para capturar errores específicos de SQLAlchemy

# Configuración directa de PostgreSQL
DB_USER = "postgres"  # Usuario de la base de datos
DB_PASS = "postgres"  # Contraseña del usuario
DB_HOST = "localhost"  # Dirección del host de la base de datos
DB_PORT = "5432"  # Puerto donde escucha PostgreSQL
DB_NAME = "autenticacion"  # Nombre de la base de datos

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

except SQLAlchemyError as e:
    raise Exception(f"Error al conectar con la base de datos: {str(e)}")

def get_db():
    db = SessionLocal()  # Se crea una nueva sesión a partir de SessionLocal
    try:
        yield db  # Se "entrega" la sesión al bloque que la necesite (por ejemplo, un endpoint)
    except SQLAlchemyError as e:
        db.rollback()  # Si ocurre un error, se hace rollback de cualquier cambio no confirmado
        raise Exception(f"Error en la operación de base de datos: {str(e)}")  # Se lanza una excepción personalizada
    finally:
        db.close()  # Siempre se cierra la sesión, haya error o no, para liberar recursos
