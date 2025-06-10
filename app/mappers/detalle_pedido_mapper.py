# app/mappers/detalle_pedido_mapper.py


from app.domain.entities.detalle_pedido_entity import DetallePedidoEntity
from app.models.detalle_pedido import DetallePedido


def to_entity(model: DetallePedido) -> DetallePedidoEntity:
    return DetallePedidoEntity(
        id=model.id,
        pedido_id=model.pedido_id,
        producto_id=model.producto_id,
        cantidad=model.cantidad,
        precio_unitario=model.precio_unitario,
    )

def to_model(entity: DetallePedidoEntity) -> DetallePedido:
    return DetallePedido(
        id=entity.id,
        pedido_id=entity.pedido_id,
        producto_id=entity.producto_id,
        cantidad=entity.cantidad,
        precio_unitario=entity.precio_unitario,
    )
