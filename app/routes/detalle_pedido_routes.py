from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.domain.detalle_pedido import DetallePedido
from app.services.dependencies import get_detalle_pedido_service
from app.services.detalle_pedido_service import DetallePedidoService

router = APIRouter(prefix="/detalles", tags=["DetallePedido"])


@router.post("/", response_model=DetallePedido)
def crear(
    detalle: DetallePedido,
    service: DetallePedidoService = Depends(get_detalle_pedido_service)
):
    return service.crear_detalle(detalle)


@router.get("/", response_model=List[DetallePedido])
def listar(service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    return service.obtener_detalles()


@router.get("/{detalle_id}", response_model=DetallePedido)
def obtener(detalle_id: int, service: DetallePedidoService = Depends(get_detalle_pedido_service)):
    detalle = service.obtener_detalle_por_id(detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle


@router.put("/{detalle_id}", response_model=DetallePedido)
def actualizar(
    detalle_id: int,
    datos: DetallePedido,
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
