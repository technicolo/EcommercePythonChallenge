import json
from datetime import date

from app.models.detalle_pedido import DetallePedido
from app.models.pedido import Pedido
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.persistence.db import create_db_and_tables, get_session
from app.services.pedido_service import PedidoService
from app.utils.security import hash_password


def cargar_seed():
    with open("seed_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    session = next(get_session())
    create_db_and_tables()

    usuarios_map = {}
    for usuario in data["usuarios"]:
        u = Usuario(nombre=usuario["nombre"], email=usuario["email"],password=hash_password(usuario["password"]))
        session.add(u)
        session.flush()
        usuarios_map[usuario["email"]] = u.id

    productos_map = {}
    for producto in data["productos"]:
        p = Producto(nombre=producto["nombre"], precio=producto["precio"], stock=producto["stock"])
        session.add(p)
        session.flush()
        productos_map[producto["nombre"]] = p.id

    pedidos = []
    for pedido in data["pedidos"]:
        user_id = usuarios_map[pedido["usuario_email"]]
        p = Pedido(
            fecha=date.fromisoformat(pedido["fecha"]),
            estado=pedido["estado"],
            usuario_id=user_id,
            total=0.0  
        )
        session.add(p)
        session.flush()
        pedidos.append(p)

    for detalle in data["detalles_pedido"]:
        pedido = pedidos[detalle["pedido_index"]]
        producto_id = productos_map[detalle["producto_nombre"]]

        # Obtener precio del producto
        producto = session.get(Producto, producto_id)
        precio_unitario = producto.precio

        d = DetallePedido(
            pedido_id=pedido.id,
            producto_id=producto_id,
            cantidad=detalle["cantidad"],
            precio_unitario=precio_unitario  # 💡 clave
        )
        session.add(d)

    session.commit()

    # Calcular total de pedidos
    servicio = PedidoService(session)
    for p in pedidos:
        servicio.actualizar_total_pedido(p.id)

    print(" Datos de prueba cargados correctamente.")

if __name__ == "__main__":
    cargar_seed()
