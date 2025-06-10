# app/services/detalle_pedido_service.py
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from app.domain.detalle_pedido import DetallePedido
from app.domain.pedido import Pedido
from app.services.pedido_service import PedidoService


class DetallePedidoService:
    def __init__(self, session: Session):
        self.session = session
        self.pedido_service = PedidoService(session)

    def crear_detalle(self, detalle: DetallePedido) -> DetallePedido:
        pedido = self.session.get(Pedido, detalle.pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado para este detalle")

        self.session.add(detalle)
        self.session.commit()
        self.session.refresh(detalle)

        # Usamos método de instancia
        self.pedido_service.actualizar_total_pedido(detalle.pedido_id)

        return detalle

    def obtener_detalles(self) -> List[DetallePedido]:
        return self.session.exec(select(DetallePedido)).all()

    def obtener_detalle_por_id(self, detalle_id: int) -> Optional[DetallePedido]:
        return self.session.get(DetallePedido, detalle_id)

    def actualizar_detalle(self, detalle_id: int, datos: DetallePedido) -> Optional[DetallePedido]:
        detalle = self.session.get(DetallePedido, detalle_id)
        if not detalle:
            return None
        detalle.pedido_id = datos.pedido_id
        detalle.producto_id = datos.producto_id
        detalle.cantidad = datos.cantidad
        detalle.precio_unitario = datos.precio_unitario
        self.session.commit()
        self.session.refresh(detalle)
        return detalle

    def eliminar_detalle(self, detalle_id: int) -> bool:
        detalle = self.session.get(DetallePedido, detalle_id)
        if not detalle:
            return False
        self.session.delete(detalle)
        self.session.commit()
        return True
