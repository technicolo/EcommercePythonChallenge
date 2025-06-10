# app/mappers/pedido_mapper.py

from app.domain.entities.pedido_entity import PedidoEntity
from app.models.pedido import Pedido


def to_entity(model: Pedido) -> PedidoEntity:
    return PedidoEntity(
        id=model.id,
        usuario_id=model.usuario_id,
        total=model.total,
        fecha=model.fecha,
    )

def to_model(entity: PedidoEntity) -> Pedido:
    return Pedido(
        id=entity.id,
        usuario_id=entity.usuario_id,
        total=entity.total,
        fecha=entity.fecha,
    )
