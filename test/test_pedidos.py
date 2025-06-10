from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.domain.detalle_pedido import DetallePedido
from app.domain.pedido import Pedido, PedidoCreate
from app.domain.usuario import Usuario
from app.persistence.db import get_session
from app.services import pedido_service


def test_crear_pedido_exitoso():
    pedido_in = PedidoCreate(usuario_id=1)
    usuario_mock = Usuario(id=1, nombre="Juan")
    pedido_mock = Pedido(id=1, usuario_id=1, fecha=datetime.utcnow(), total=0)

    with patch("app.services.pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = usuario_mock
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda x: x
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = pedido_service.crear_pedido(pedido_in)

        assert resultado.usuario_id == pedido_mock.usuario_id
        assert resultado.total == 0


def test_obtener_pedidos_con_y_sin_filtro():
    pedidos_mock = [
        Pedido(id=1, usuario_id=1, fecha=datetime(2025, 6, 1), total=100),
        Pedido(id=2, usuario_id=2, fecha=datetime(2025, 6, 2), total=200),
    ]

    with patch("app.services.pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.exec.return_value.all.return_value = pedidos_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = pedido_service.obtener_pedidos()
        assert len(resultado) == 2


def test_actualizar_total_pedido_suma_correctamente():
    detalles_mock = [
        DetallePedido(pedido_id=1, producto_id=1, cantidad=2, precio_unitario=100),
        DetallePedido(pedido_id=1, producto_id=2, cantidad=1, precio_unitario=300),
    ]
    pedido_mock = Pedido(id=1, usuario_id=1, total=0, fecha=datetime.utcnow())

    with patch("app.services.pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()

        # Simula el .all() correctamente
        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = detalles_mock
        mock_session.exec.return_value = mock_exec_result

        mock_session.get.return_value = pedido_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        pedido_service.actualizar_total_pedido(1)
        assert pedido_mock.total == 500




def actualizar_pedido(pedido_id: int, datos: PedidoCreate):
    with get_session() as session:  # type: ignore
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        pedido.usuario_id = datos.usuario_id
        # No intentes acceder a datos.total si no está definido en PedidoCreate

        session.add(pedido)
        session.commit()
        session.refresh(pedido)
        return pedido


def test_actualizar_pedido_no_existente():
    with patch("app.services.pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = None
        mock_get_session.return_value.__enter__.return_value = mock_session

        with pytest.raises(HTTPException) as exc_info:
            pedido_service.actualizar_pedido(99, PedidoCreate(usuario_id=1))

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Pedido no encontrado"


def test_eliminar_pedido_existente():
    pedido_mock = Pedido(id=1, usuario_id=1, fecha=datetime.utcnow(), total=100)

    with patch("app.services.pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = pedido_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = pedido_service.eliminar_pedido(1)
        assert resultado is True


def test_eliminar_pedido_no_existente():
    with patch("app.services.pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = None
        mock_get_session.return_value.__enter__.return_value = mock_session

        with pytest.raises(HTTPException) as exc_info:
            pedido_service.eliminar_pedido(999)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Pedido no encontrado"
