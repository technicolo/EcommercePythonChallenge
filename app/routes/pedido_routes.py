# app/routes/pedidos_routes.py

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Request,  # necesario para usar request.state
)
from sqlmodel import Session

from app.dependencies.auth import get_current_user
from app.domain.entities.pedido_entity import PedidoEntity
from app.models.detalle_pedido import PedidoConDetallesDTO
from app.models.pedido import PedidoCreate
from app.models.usuario import Usuario
from app.persistence.db import get_session
from app.services.dependencies import get_pedido_service
from app.services.pedido_service import PedidoService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=PedidoEntity)
def crear_pedido(
    pedido: PedidoCreate,
    service: PedidoService = Depends(get_pedido_service),
    user: Usuario = Depends(get_current_user),
):
    return service.crear_pedido(pedido)


@router.get("/", response_model=List[PedidoEntity])
def listar(fecha_inicio: Optional[datetime] = Query(None),fecha_fin: Optional[datetime] = Query(None),service: PedidoService = Depends(get_pedido_service),request: Request = None):
    logger.info(f"[{request.state.correlation_id}] Listando pedidos desde {fecha_inicio} hasta {fecha_fin}")
    return service.obtener_pedidos(fecha_inicio, fecha_fin)



@router.get("/{pedido_id}", response_model=PedidoConDetallesDTO)
def obtener_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    return service.obtener_pedido_con_detalles(pedido_id)


@router.put("/{pedido_id}", response_model=PedidoEntity)
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

@router.post("/{pedido_id}/pagar")
def pagar_pedido(pedido_id: int, session: Session = Depends(get_session)):
    service = PedidoService(session)
    try:
        pedido_actualizado = service.pagar_pedido(pedido_id)
        return pedido_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))