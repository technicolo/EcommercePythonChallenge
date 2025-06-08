from fastapi import APIRouter, HTTPException
from typing import List
from app.domain.detalle_pedido import DetallePedido
from app.services import detalle_pedido_service

router = APIRouter(prefix="/detalles", tags=["DetallePedido"])


@router.post("/", response_model=DetallePedido)
def crear(detalle: DetallePedido):
    return detalle_pedido_service.crear_detalle(detalle)


@router.get("/", response_model=List[DetallePedido])
def listar():
    return detalle_pedido_service.obtener_detalles()


@router.get("/{detalle_id}", response_model=DetallePedido)
def obtener(detalle_id: int):
    detalle = detalle_pedido_service.obtener_detalle_por_id(detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.put("/{detalle_id}", response_model=DetallePedido)
def actualizar(detalle_id: int, datos: DetallePedido):
    detalle = detalle_pedido_service.actualizar_detalle(detalle_id, datos)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.delete("/{detalle_id}")
def eliminar(detalle_id: int):
    if not detalle_pedido_service.eliminar_detalle(detalle_id):
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"mensaje": "Detalle eliminado"}
