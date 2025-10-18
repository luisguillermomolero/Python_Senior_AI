from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Cliente(BaseModel):
    id: int
    nombre: str
    edad: int

clientes_db: List[Cliente] = []
contador_id = 1

@app.get("/")
def root():
    return {"mensaje": "bienvenidos"}

@app.post("/clientes", response_model=Cliente)
def crear_cliente(cliente: Cliente):
    global contador_id
    cliente.id = contador_id
    clientes_db.append(cliente)
    contador_id += 1
    return cliente

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    return clientes_db

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    for cliente in clientes_db:
        if cliente.id == cliente_id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente: Cliente):
    for i, c in enumerate(clientes_db):
        if c.id == cliente_id:
            cliente.id = cliente_id
            clientes_db[i] = cliente
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    for i, cliente in enumerate(clientes_db):
        if cliente.id == cliente_id:
            clientes_db.pop(i)
            return {"mensaje": f"Cliente con ID {cliente_id} eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")