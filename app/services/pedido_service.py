# app/services/pedido_service.py

from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from app.domain.entities.pedido_entity import PedidoEntity
from app.mappers.pedido_mapper import to_entity
from app.models.detalle_pedido import (
    DetallePedido,
    DetallePedidoDTO,
    PedidoConDetallesDTO,
)
from app.models.pedido import Pedido, PedidoCreate
from app.models.usuario import Usuario
from app.utils.ProblemDetailsException import problem_detail_response


class PedidoService:
    def __init__(self, session: Session):
        self.session = session

    def crear_pedido(self, pedido_in: PedidoCreate) -> PedidoEntity:
        usuario = self.session.get(Usuario, pedido_in.usuario_id)
        if not usuario:
            raise problem_detail_response(
                status_code=404,
                title="Recurso no encontrado",
                detail="Usuario no encontrado",
                instance="/pedidos"
            )

        model = Pedido(usuario_id=pedido_in.usuario_id, fecha=datetime.utcnow(), total=0)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_entity(model)

    def obtener_pedidos(self, fecha_inicio: Optional[datetime] = None, fecha_fin: Optional[datetime] = None) -> List[PedidoEntity]:
        query = select(Pedido)
        if fecha_inicio:
            query = query.where(Pedido.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.where(Pedido.fecha <= fecha_fin)
        results = self.session.exec(query).all()
        return [to_entity(p) for p in results]

    def obtener_pedido_con_detalles(self, pedido_id: int) -> PedidoConDetallesDTO:
        pedido = self.session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        detalles = self.session.exec(
            select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        ).all()

        detalles_dto = [
            DetallePedidoDTO(
                producto_id=d.producto_id,
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario
            ) for d in detalles
        ]

        return PedidoConDetallesDTO(
            id=pedido.id,
            usuario_id=pedido.usuario_id,
            total=pedido.total,
            fecha=pedido.fecha,
            detalles=detalles_dto
        )

    def actualizar_pedido(self, pedido_id: int, datos: PedidoCreate) -> Optional[PedidoEntity]:
        pedido = self.session.get(Pedido, pedido_id)
        if not pedido:
            return None
        pedido.usuario_id = datos.usuario_id
        self.session.commit()
        self.session.refresh(pedido)
        return to_entity(pedido)

    def eliminar_pedido(self, pedido_id: int) -> bool:
        pedido = self.session.get(Pedido, pedido_id)
        if not pedido:
            return False
        self.session.delete(pedido)
        self.session.commit()
        return True

    def obtener_pedidos_por_usuario(self, usuario_id: int) -> List[PedidoEntity]:
        query = select(Pedido).where(Pedido.usuario_id == usuario_id)
        results = self.session.exec(query).all()
        return [to_entity(p) for p in results]

    def actualizar_total_pedido(self, pedido_id: int) -> None:
        detalles = self.session.exec(
            select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        ).all()

        total = sum(d.cantidad * d.precio_unitario for d in detalles)
        pedido = self.session.get(Pedido, pedido_id)
        if not pedido:
            raise problem_detail_response(
                status_code=404,
                title="Recurso no encontrado",
                detail="Pedido no encontrado al actualizar total",
                instance=f"/pedidos/{pedido_id}/actualizar-total"
            )
        pedido.total = total
        self.session.commit()
