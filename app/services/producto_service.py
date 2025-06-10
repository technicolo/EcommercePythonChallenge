# app/services/producto_service.py
from typing import List, Optional

from sqlmodel import Session, select

from app.domain.producto import Producto


class ProductoService:
    def __init__(self, session: Session):
        self.session = session

    def crear_producto(self, producto: Producto) -> Producto:
        self.session.add(producto)
        self.session.commit()
        self.session.refresh(producto)
        return producto

    def obtener_productos(self) -> List[Producto]:
        productos = self.session.exec(select(Producto)).all()
        return productos

    def obtener_producto_por_id(self, producto_id: int) -> Optional[Producto]:
        return self.session.get(Producto, producto_id)

    def actualizar_producto(self, producto_id: int, datos_actualizados: Producto) -> Optional[Producto]:
        producto = self.session.get(Producto, producto_id)
        if not producto:
            return None
        producto.nombre = datos_actualizados.nombre
        producto.precio = datos_actualizados.precio
        producto.stock = datos_actualizados.stock
        self.session.commit()
        self.session.refresh(producto)
        return producto

    def eliminar_producto(self, producto_id: int) -> bool:
        producto = self.session.get(Producto, producto_id)
        if not producto:
            return False
        self.session.delete(producto)
        self.session.commit()
        return True
