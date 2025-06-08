from fastapi import APIRouter, HTTPException
from typing import List
from app.domain.producto import Producto
from app.services import producto_service

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
