from app.models.detalle_pedido import DetallePedido
from app.models.pedido import Pedido
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.persistence.db import get_session


def limpiar_datos():
    session = next(get_session())

    # Borrar en orden para respetar claves foráneas
    session.query(DetallePedido).delete()
    session.query(Pedido).delete()
    session.query(Producto).delete()
    session.query(Usuario).delete()

    session.commit()
    print("🧹 Todas las tablas fueron vaciadas correctamente.")

if __name__ == "__main__":
    limpiar_datos()
