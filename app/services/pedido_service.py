from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException

from app.domain.pedido import Pedido, PedidoCreate
from app.domain.detalle_pedido import DetallePedido, PedidoConDetallesDTO, DetallePedidoDTO
from app.domain.usuario import Usuario
from app.persistence.db import get_session
from app.utils.ProblemDetailsException  import problem_detail_response

def crear_pedido(pedido_in: PedidoCreate) -> Pedido:
    with get_session() as session:
        usuario = session.get(Usuario, pedido_in.usuario_id)
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
            total=0  # Se inicializa en 0
        )
        session.add(pedido)
        session.commit()
        session.refresh(pedido)
        return pedido



def obtener_pedidos(fecha_inicio: Optional[datetime] = None, fecha_fin: Optional[datetime] = None) -> List[Pedido]:
    with get_session() as session:
        query = select(Pedido)

        if fecha_inicio:
            query = query.where(Pedido.fecha >= fecha_inicio)
        if fecha_fin:
            query = query.where(Pedido.fecha <= fecha_fin)

        return session.exec(query).all()


def obtener_pedidos_con_detalles_por_usuario(usuario_id: int) -> List[PedidoConDetallesDTO]:
    with get_session() as session:
        pedidos = session.exec(
            select(Pedido).where(Pedido.usuario_id == usuario_id)
        ).all()

        resultado = []

        for pedido in pedidos:
            detalles = session.exec(
                select(DetallePedido).where(DetallePedido.pedido_id == pedido.id)
            ).all()

            detalles_dto = [
                DetallePedidoDTO(
                    producto_id=d.producto_id,
                    cantidad=d.cantidad,
                    precio_unitario=d.precio_unitario
                )
                for d in detalles
            ]

            pedido_con_detalles = PedidoConDetallesDTO(
                id=pedido.id,
                usuario_id=pedido.usuario_id,
                total=pedido.total,
                fecha=pedido.fecha,
                detalles=detalles_dto
            )

            resultado.append(pedido_con_detalles)

        return resultado


def actualizar_pedido(pedido_id: int, datos_actualizados: PedidoCreate) -> Pedido:
    with get_session() as session:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise problem_detail_response(
                status_code=404,
                title="Recurso no encontrado",
                detail="Pedido no encontrado",
                instance=f"/pedidos/{pedido_id}"
            )
        pedido.total = datos_actualizados.total
        pedido.usuario_id = datos_actualizados.usuario_id
        session.commit()
        session.refresh(pedido)
        return pedido
    

def eliminar_pedido(pedido_id: int) -> None:
    with get_session() as session:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise problem_detail_response(
                status_code=404,
                title="Recurso no encontrado",
                detail="Pedido no encontrado",
                instance=f"/pedidos/{pedido_id}"
            )
        session.delete(pedido)
        session.commit()


def obtener_pedidos_por_usuario(usuario_id: int) -> List[Pedido]:
    with get_session() as session:
        query = select(Pedido).where(Pedido.usuario_id == usuario_id)
        results = session.exec(query).all()
        return results


def actualizar_total_pedido(pedido_id: int) -> None:
    with get_session() as session:
        detalles = session.exec(
            select(DetallePedido).where(DetallePedido.pedido_id == pedido_id)
        ).all()

        total = sum(d.cantidad * d.precio_unitario for d in detalles)

        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise problem_detail_response(
                status_code=404,
                title="Recurso no encontrado",
                detail="Pedido no encontrado al actualizar total",
                instance=f"/pedidos/{pedido_id}/actualizar-total"
            )
        pedido.total = total
        session.commit()
