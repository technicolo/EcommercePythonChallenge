from fastapi import APIRouter, HTTPException
from typing import List
from app.domain.producto import Producto
from app.services import producto_service
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.csv_parser import parse_csv_to_productos
from app.persistence.db import get_session

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=Producto)
def crear(producto: Producto):
    return producto_service.crear_producto(producto)


@router.get("/", response_model=List[Producto])
def listar():
    return producto_service.obtener_productos()


@router.get("/{producto_id}", response_model=Producto)
def obtener(producto_id: int):
    producto = producto_service.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=Producto)
def actualizar(producto_id: int, datos: Producto):
    producto = producto_service.actualizar_producto(producto_id, datos)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/{producto_id}")
def eliminar(producto_id: int):
    if not producto_service.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}

@router.post("/importar-csv")
async def importar_productos_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    content = (await file.read()).decode("utf-8")
    productos = parse_csv_to_productos(content)

    with get_session() as session:
        session.add_all(productos)
        session.commit()

    return {"mensaje": f"Se importaron {len(productos)} productos correctamente"}