from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.domain.usuario import Usuario
from app.domain.detalle_pedido import PedidoConDetallesDTO
from app.services.usuario_service import UsuarioService
from app.services.pedido_service import PedidoService
from app.services.dependencies import get_usuario_service, get_pedido_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=Usuario)
def crear(usuario: Usuario, service: UsuarioService = Depends(get_usuario_service)):
    return service.crear_usuario(usuario)


@router.get("/", response_model=List[Usuario])
def listar(service: UsuarioService = Depends(get_usuario_service)):
    return service.obtener_usuarios()


@router.get("/{usuario_id}", response_model=Usuario)
def obtener(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):
    usuario = service.obtener_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=Usuario)
def actualizar(usuario_id: int, datos: Usuario, service: UsuarioService = Depends(get_usuario_service)):
    usuario = service.actualizar_usuario(usuario_id, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{usuario_id}")
def eliminar(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):
    if not service.eliminar_usuario(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"mensaje": "Usuario eliminado"}


@router.get("/{usuario_id}/pedidos", response_model=List[PedidoConDetallesDTO])
def listar_pedidos_usuario(
    usuario_id: int,
    service: PedidoService = Depends(get_pedido_service)
):
    return service.obtener_pedidos_con_detalles_por_usuario(usuario_id)
