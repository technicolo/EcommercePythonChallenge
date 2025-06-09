from fastapi import Depends
from sqlmodel import Session
from app.persistence.db import get_session
from app.services.pedido_service import PedidoService
from app.services.producto_service import ProductoService
from app.services.detalle_pedido_service import DetallePedidoService
# app/services/dependencies.py
from app.services.usuario_service import UsuarioService

def get_pedido_service(session: Session = Depends(get_session)) -> PedidoService:
    return PedidoService(session)

def get_producto_service(session: Session = Depends(get_session)) -> ProductoService:
    return ProductoService(session)



def get_detalle_pedido_service(session: Session = Depends(get_session)) -> DetallePedidoService:
    return DetallePedidoService(session)


def get_usuario_service(session: Session = Depends(get_session)) -> UsuarioService:
    return UsuarioService(session)