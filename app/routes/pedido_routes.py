from fastapi import APIRouter, HTTPException
from typing import List
from app.domain.pedido import Pedido, PedidoCreate
from app.services import pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("/", response_model=Pedido)
def crear(pedido: PedidoCreate):
    return pedido_service.crear_pedido(pedido)


@router.get("/", response_model=List[Pedido])
def listar():
    return pedido_service.obtener_pedidos()


@router.get("/{pedido_id}", response_model=Pedido)
def obtener(pedido_id: int):
    pedido = pedido_service.obtener_pedido_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


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
