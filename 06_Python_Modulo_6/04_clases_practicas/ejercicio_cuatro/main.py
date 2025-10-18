from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional
import uuid # Identificador Único Universal

app = FastAPI(
    title="API de productos",
    description="API para generar productos con FastAPI y Pydantic"
)

# Modelo/Clase base => herencia de BaseModel
class ProductoBase(BaseModel):
    nombre: str
    precio: float

# Modelo/Clase que se usa para crear nuevos productos
class ProductoCrear(ProductoBase):
    pass

# Modelo/Clase para actualizar productos
class ProductoActualizar(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None

# Modelo/Clase
class ProductoRespuesta(ProductoBase):
    id: str

productos: Dict[str, dict] = {}

@app.get("/")
async def raiz():
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "mensaje":"Bienvenido a la API de productos"
        }
    )

@app.post("/productos/")
async def crear_producto(producto: ProductoCrear):
    producto_id = str(uuid.uuid4()) # "sd4fg8sd7fg65d4fg687d6fg4d68fg6d8f"
    nuevo_producto = producto.model_dump() # objeto: nombre, precio => {"nombre": Luis, "precio": 45.20}
    productos[producto_id] = nuevo_producto # {"id": "ff4s5d4s8df56s4", {"nombre": Luis, "precio": 45.20}}
    
    return JSONResponse(
        status_code=201,
        content={
            "exito": True,
            "mensaje": "Producto creado",
            "producto": ProductoRespuesta(id=producto_id, **nuevo_producto).model_dump()
        }
    )
    
@app.get("/productos/")
async def obtener_productos():
    if not productos:
        return JSONResponse(
            status_code=404,
            content={
                "exitos": False,
                "mensaje": "No hay productos registrados",
                "produtos": []
            }
        )
    
    lista_productos = [
        ProductoRespuesta(id=pid, **data).model_dump()
        for pid, data in productos.items()
    ]
    
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "productos": lista_productos
        }
    )

@app.get("/productos/{producto_id}")
async def obtener_producto(producto_id: str):
    if producto_id not in productos:
        return JSONResponse(
            status_code=404,
            content={
                "exitos": False,
                "mensaje":"No existe el producto"
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "producto": ProductoRespuesta(id=producto_id, **productos[producto_id]).model_dump()
        }
    )

@app.put("/productos/{producto_id}")
async def actualizar_producto(producto_id: str, producto_actualizar: ProductoActualizar):
    if producto_id not in productos:
        return JSONResponse(
            status_code=404,
            content={
                "exitos": False,
                "mensaje":"No existe el producto"
            }
        )
    
    producto_existente = productos[producto_id]
    datos_actualizados = producto_actualizar.model_dump(exclude_unset=True)
    producto_existente.update(datos_actualizados)
    productos[producto_id] = producto_existente
    
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "mensaje": "Producto actualizado",
            "producto": ProductoRespuesta(id=producto_id, **producto_existente).model_dump()
        }
    )

@app.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: str):
    if producto_id not in productos:
        return JSONResponse(
            status_code=404,
            content={
                "exito": False,
                "mensaje":"No existe el producto"
            }
        )
    
    producto_eliminado = productos.pop(producto_id)
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "mensaje": f"Producto con id {producto_id} eliminado exitosamente",
            "producto": ProductoRespuesta(id=producto_id, **producto_eliminado).model_dump()
        }
    )

