from fastapi import APIRouter, HTTPException
from typing import List
from app.domain.detalle_pedido import PedidoConDetallesDTO
from app.domain.usuario import Usuario
from app.services import usuario_service
from app.domain.pedido import Pedido
from app.services import pedido_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=Usuario)
def crear(usuario: Usuario):
    return usuario_service.crear_usuario(usuario)


@router.get("/", response_model=List[Usuario])
def listar():
    return usuario_service.obtener_usuarios()


@router.get("/{usuario_id}", response_model=Usuario)
def obtener(usuario_id: int):
    usuario = usuario_service.obtener_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=Usuario)
def actualizar(usuario_id: int, datos: Usuario):
    usuario = usuario_service.actualizar_usuario(usuario_id, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{usuario_id}")
def eliminar(usuario_id: int):
    if not usuario_service.eliminar_usuario(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}

@router.get("/{usuario_id}/pedidos", response_model=List[PedidoConDetallesDTO])
def listar_pedidos_usuario(usuario_id: int):
    return pedido_service.obtener_pedidos_con_detalles_por_usuario(usuario_id)