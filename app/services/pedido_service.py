# app/services/pedido_service.py
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException
from app.domain.pedido import Pedido, PedidoCreate
from app.domain.detalle_pedido import DetallePedido, PedidoConDetallesDTO, DetallePedidoDTO
from app.domain.usuario import Usuario
from app.utils.ProblemDetailsException import problem_detail_response

class PedidoService:
    def __init__(self, session: Session):
        self.session = session

    def crear_pedido(self, pedido_in: PedidoCreate) -> Pedido:
        usuario = self.session.get(Usuario, pedido_in.usuario_id)
        if not usuario:
            raise problem_detail_response(
                status_code=404,
                title="Recurso no encontrado",
                detail="Usuario no encontrado",
                instance="/pedidos"
            )

        pedido = Pedido(
            usuario_id=pedido_in.usuario_id,
            fecha=datetime.utcnow(),
            total=0
        )
        self.session.add(pedido)
        self.session.commit()
        self.session.refresh(pedido)
        return pedido

    def obtener_pedidos(self, fecha_inicio: Optional[datetime] = None, fecha_fin: Optional[datetime] = None) -> List[Pedido]:
        query = select(Pedido)
        if fecha_inicio:
            query = query.where(Pedido.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.where(Pedido.fecha <= fecha_fin)
        return self.session.exec(query).all()

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

    def actualizar_pedido(self, pedido_id: int, datos: PedidoCreate) -> Optional[Pedido]:
        pedido = self.session.get(Pedido, pedido_id)
        if not pedido:
            return None
        pedido.usuario_id = datos.usuario_id
        self.session.commit()
        self.session.refresh(pedido)
        return pedido

    def eliminar_pedido(self, pedido_id: int) -> bool:
        pedido = self.session.get(Pedido, pedido_id)
        if not pedido:
            return False
        self.session.delete(pedido)
        self.session.commit()
        return True

    def obtener_pedidos_por_usuario(self, usuario_id: int) -> List[Pedido]:
        query = select(Pedido).where(Pedido.usuario_id == usuario_id)
        return self.session.exec(query).all()

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
