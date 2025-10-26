# app/main.py

# Importamos FastAPI para crear la aplicación web y HTTPException para manejo de errores
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# Importamos middleware de CORS para permitir peticiones desde otros dominios
from fastapi.middleware.cors import CORSMiddleware

# Importamos la base declarativa y el motor de la base de datos
from core.database import Base, engine

# Importamos el modelo User para que se cree la tabla
from models.user_model import User

# Importamos las rutas de usuario con un alias
from routes.user_routes import router as user_router

# Importamos logging para registrar mensajes en consola o archivos
import logging

# Importamos contextlib para manejar eventos de ciclo de vida
from contextlib import asynccontextmanager

# ------------------------------------------------------------
# Configuración del sistema de logging para monitoreo de errores
logging.basicConfig(
    level=logging.INFO,  # Nivel de registro (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Formato del mensaje
)
logger = logging.getLogger(__name__)  # Creamos un logger específico para este archivo

# ------------------------------------------------------------
# Gestor de eventos de ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el inicio y cierre de la aplicación"""
    # Código que se ejecuta al iniciar
    try:
        Base.metadata.create_all(bind=engine)  # Ejecuta la creación de todas las tablas definidas en los modelos
        logger.info("Base de datos inicializada correctamente")  # Mensaje de éxito
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")  # Mensaje de error
        raise  # Lanza nuevamente la excepción para detener la aplicación si hay fallo
    
    yield  # Aquí la aplicación está en ejecución
    
    # Código que se ejecuta al cerrar (si fuera necesario en el futuro)
    logger.info("Aplicación finalizando...")

# ------------------------------------------------------------
# Instancia principal de la aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Cuentas",  # Título que aparecerá en la documentación Swagger
    description="API para gestión de usuarios con autenticación JWT",  # Descripción de la API
    version="1.0.0",  # Versión de la API
    lifespan=lifespan  # Gestor de ciclo de vida
)

# ------------------------------------------------------------
# Middleware para permitir CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen (¡modificar en producción!)
    allow_credentials=True,  # Permite el envío de cookies o credenciales
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados personalizados
)

# ------------------------------------------------------------
# Manejador global de errores no controlados
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error no manejado: {str(exc)}")  # Registra el error
    return JSONResponse(
        status_code=500,  # Error interno del servidor
        content={"detail": "Error interno del servidor"}
    )

# ------------------------------------------------------------
# Incluir el conjunto de rutas definidas en el archivo user_routes
app.include_router(user_router, prefix="/api/v1")  # Todas las rutas estarán bajo /api/v1 (ej: /api/v1/login)

# ------------------------------------------------------------
# Punto de entrada principal de la aplicación
def main():
    """Función principal para iniciar el servidor"""
    import uvicorn
    import webbrowser
    from threading import Timer
    
    host = "127.0.0.1"
    port = 8000
    
    # Abrir navegador automáticamente después de 1.5 segundos
    def open_browser():
        webbrowser.open(f"http://{host}:{port}/docs")
    
    Timer(1.5, open_browser).start()
    
    # Ejecutar servidor uvicorn con hot-reload
    uvicorn.run(
        "main:app",  # Módulo:aplicación
        host=host,  # Escucha en localhost
        port=port,  # Puerto del servidor
        reload=True,  # Hot-reload activado para desarrollo
        log_level="info"  # Nivel de logs
    )

if __name__ == "__main__":
    main()
