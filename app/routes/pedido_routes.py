from fastapi import APIRouter, HTTPException, UploadFile, File, Query, Depends
from typing import List, Optional
from datetime import datetime

from app.domain.pedido import Pedido, PedidoCreate
from app.domain.detalle_pedido import PedidoConDetallesDTO
from app.services.dependencies import get_pedido_service
from app.services.pedido_service import PedidoService

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=Pedido)
def crear(pedido: PedidoCreate, service: PedidoService = Depends(get_pedido_service)):
    return service.crear_pedido(pedido)


@router.get("/", response_model=List[Pedido])
def listar(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.obtener_pedidos(fecha_inicio, fecha_fin)


@router.get("/{pedido_id}", response_model=PedidoConDetallesDTO)
def obtener_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    return service.obtener_pedido_con_detalles(pedido_id)


@router.put("/{pedido_id}", response_model=Pedido)
def actualizar(pedido_id: int, datos: PedidoCreate, service: PedidoService = Depends(get_pedido_service)):
    pedido = service.actualizar_pedido(pedido_id, datos)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.delete("/{pedido_id}")
def eliminar(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    if not service.eliminar_pedido(pedido_id):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado"}
