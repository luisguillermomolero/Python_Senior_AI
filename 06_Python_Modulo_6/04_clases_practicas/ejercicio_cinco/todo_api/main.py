from fastapi import FastAPI
from routes import router as tareas_router

app = FastAPI()

@app.get("/")
def root():
    return "Bienvenidos a mi API TO-DO List"

app.include_router(
    tareas_router,
    prefix="/api",
    tags=["tareas"]
)