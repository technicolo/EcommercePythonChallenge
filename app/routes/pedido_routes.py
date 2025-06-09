from fastapi import APIRouter, HTTPException,APIRouter,UploadFile, File,Query
from typing import List,Optional
from app.domain.pedido import Pedido, PedidoCreate
from app.services import pedido_service 
from app.domain.detalle_pedido import PedidoConDetallesDTO
from app.utils.csv_parser import parse_csv_to_productos
from app.persistence.db import get_session
from datetime import datetime


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=Pedido)
def crear(pedido: PedidoCreate):
    return pedido_service.crear_pedido(pedido)


@router.get("/", response_model=List[Pedido])
def listar(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
):
    return pedido_service.obtener_pedidos(fecha_inicio, fecha_fin)


@router.get("/{pedido_id}", response_model=PedidoConDetallesDTO)
def obtener_pedido(pedido_id: int):
    return pedido_service.obtener_pedido_con_detalles(pedido_id)


@router.put("/{pedido_id}", response_model=Pedido)
def actualizar(pedido_id: int, datos: PedidoCreate):
    pedido = pedido_service.actualizar_pedido(pedido_id, datos)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.delete("/{pedido_id}")
def eliminar(pedido_id: int):
    if not pedido_service.eliminar_pedido(pedido_id):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado"}



productos_router = APIRouter(prefix="/productos", tags=["Productos"])


