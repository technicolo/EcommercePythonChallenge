from sqlmodel import Session, select
from app.domain.detalle_pedido import DetallePedido
from app.persistence.db import get_session
from typing import List, Optional
from app.services.pedido_service import actualizar_total_pedido
from fastapi import HTTPException
from app.domain.pedido import Pedido



def crear_detalle(detalle: DetallePedido) -> DetallePedido:
    with get_session() as session:
        pedido = session.get(Pedido, detalle.pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado para este detalle")

        session.add(detalle)
        session.commit()
        session.refresh(detalle)
        actualizar_total_pedido(detalle.pedido_id)
        return detalle



def obtener_detalles() -> List[DetallePedido]:
    with get_session() as session:
        return session.exec(select(DetallePedido)).all()


def obtener_detalle_por_id(detalle_id: int) -> Optional[DetallePedido]:
    with get_session() as session:
        return session.get(DetallePedido, detalle_id)


def actualizar_detalle(detalle_id: int, datos_actualizados: DetallePedido) -> Optional[DetallePedido]:
    with get_session() as session:
        detalle = session.get(DetallePedido, detalle_id)
        if not detalle:
            return None
        detalle.pedido_id = datos_actualizados.pedido_id
        detalle.producto_id = datos_actualizados.producto_id
        detalle.cantidad = datos_actualizados.cantidad
        detalle.precio_unitario = datos_actualizados.precio_unitario
        session.commit()
        session.refresh(detalle)
        return detalle


def eliminar_detalle(detalle_id: int) -> bool:
    with get_session() as session:
        detalle = session.get(DetallePedido, detalle_id)
        if not detalle:
            return False
        session.delete(detalle)
        session.commit()
        return True
