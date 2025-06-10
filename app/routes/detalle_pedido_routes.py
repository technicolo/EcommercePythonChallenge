# app/routes/detalle_pedido_routes.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.domain.entities.detalle_pedido_entity import DetallePedidoEntity
from app.services.dependencies import get_detalle_pedido_service
from app.services.detalle_pedido_service import DetallePedidoService

router = APIRouter(prefix="/detalles", tags=["DetallePedido"])


@router.post("/", response_model=DetallePedidoEntity)
def crear(
    detalle: DetallePedidoEntity,
    service: DetallePedidoService = Depends(get_detalle_pedido_service)
):
    return service.crear_detalle(detalle)


@router.get("/", response_model=List[DetallePedidoEntity])
def listar(service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    return service.obtener_detalles()


@router.get("/{detalle_id}", response_model=DetallePedidoEntity)
def obtener(detalle_id: int, service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    detalle = service.obtener_detalle_por_id(detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.put("/{detalle_id}", response_model=DetallePedidoEntity)
def actualizar(
    detalle_id: int,
    datos: DetallePedidoEntity,
    service: DetallePedidoService = Depends(get_detalle_pedido_service)
):
    detalle = service.actualizar_detalle(detalle_id, datos)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.delete("/{detalle_id}")
def eliminar(detalle_id: int, service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    if not service.eliminar_detalle(detalle_id):
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"mensaje": "Detalle eliminado"}
