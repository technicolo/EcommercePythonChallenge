from sqlmodel import Session, select
from app.domain.pedido import Pedido, PedidoCreate
from app.persistence.db import get_session
from typing import List, Optional
from datetime import datetime


def crear_pedido(pedido_in: PedidoCreate) -> Pedido:
    with get_session() as session:
        # Validar que el usuario existe (opcional si querés prevenir errores)
        result = session.exec(select(Pedido).where(Pedido.usuario_id == pedido_in.usuario_id)).all()

        pedido = Pedido(
            fecha=datetime.utcnow(),
            total=pedido_in.total,
            usuario_id=pedido_in.usuario_id
        )
        session.add(pedido)
        session.commit()
        session.refresh(pedido)
        return pedido


def obtener_pedidos() -> List[Pedido]:
    with get_session() as session:
        return session.exec(select(Pedido)).all()


def obtener_pedido_por_id(pedido_id: int) -> Optional[Pedido]:
    with get_session() as session:
        return session.get(Pedido, pedido_id)


def actualizar_pedido(pedido_id: int, datos_actualizados: PedidoCreate) -> Optional[Pedido]:
    with get_session() as session:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            return None
        pedido.total = datos_actualizados.total
        pedido.usuario_id = datos_actualizados.usuario_id
        session.commit()
        session.refresh(pedido)
        return pedido


def eliminar_pedido(pedido_id: int) -> bool:
    with get_session() as session:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            return False
        session.delete(pedido)
        session.commit()
        return True
