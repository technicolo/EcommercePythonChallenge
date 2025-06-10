# app/services/producto_service.py

from typing import List, Optional

from sqlmodel import Session, select

from app.domain.entities.producto_entity import ProductoEntity
from app.mappers.producto_mapper import to_entity, to_model
from app.models.producto import Producto


class ProductoService:
    def __init__(self, session: Session):
        self.session = session

    def crear_producto(self, producto: ProductoEntity) -> ProductoEntity:
        model = to_model(producto)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return to_entity(model)

    def obtener_productos(self) -> List[ProductoEntity]:
        productos = self.session.exec(select(Producto)).all()
        return [to_entity(p) for p in productos]

    def obtener_producto_por_id(self, producto_id: int) -> Optional[ProductoEntity]:
        producto = self.session.get(Producto, producto_id)
        return to_entity(producto) if producto else None

    def actualizar_producto(self, producto_id: int, datos_actualizados: ProductoEntity) -> Optional[ProductoEntity]:
        producto = self.session.get(Producto, producto_id)
        if not producto:
            return None
        producto.nombre = datos_actualizados.nombre
        producto.precio = datos_actualizados.precio
        producto.stock = datos_actualizados.stock
        self.session.commit()
        self.session.refresh(producto)
        return to_entity(producto)

    def eliminar_producto(self, producto_id: int) -> bool:
        producto = self.session.get(Producto, producto_id)
        if not producto:
            return False
        self.session.delete(producto)
        self.session.commit()
        return True
