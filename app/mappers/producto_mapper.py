# app/mappers/producto_mapper.py

from app.domain.entities.producto_entity import ProductoEntity
from app.models.producto import Producto


def to_entity(model: Producto) -> ProductoEntity:
    return ProductoEntity(
        id=model.id,
        nombre=model.nombre,
        precio=model.precio,
        stock=model.stock,
    )

def to_model(entity: ProductoEntity) -> Producto:
    return Producto(
        id=entity.id,
        nombre=entity.nombre,
        precio=entity.precio,
        stock=entity.stock,
    )
