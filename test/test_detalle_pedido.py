from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.domain.detalle_pedido import DetallePedido
from app.domain.pedido import Pedido
from app.services import detalle_pedido_service


def test_crear_detalle_exitoso():
    detalle_nuevo = DetallePedido(pedido_id=1, producto_id=2, cantidad=3, precio_unitario=50.0)
    pedido_mock = Pedido(id=1, usuario_id=1, total=0, fecha=datetime.now())

    with patch("app.services.detalle_pedido_service.get_session") as mock_get_session, \
         patch("app.services.detalle_pedido_service.actualizar_total_pedido") as mock_actualizar:

        mock_session = MagicMock()
        mock_session.get.return_value = pedido_mock
        mock_session.refresh.side_effect = lambda d: d
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = detalle_pedido_service.crear_detalle(detalle_nuevo)

        assert resultado == detalle_nuevo
        mock_actualizar.assert_called_once_with(1)


def test_crear_detalle_pedido_inexistente():
    detalle_nuevo = DetallePedido(pedido_id=99, producto_id=2, cantidad=3, precio_unitario=50.0)

    with patch("app.services.detalle_pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = None  # No encuentra el pedido
        mock_get_session.return_value.__enter__.return_value = mock_session

        with pytest.raises(HTTPException) as exc_info:
            detalle_pedido_service.crear_detalle(detalle_nuevo)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Pedido no encontrado para este detalle"


def test_obtener_detalles():
    detalles_mock = [
        DetallePedido(id=1, pedido_id=1, producto_id=2, cantidad=1, precio_unitario=100.0),
        DetallePedido(id=2, pedido_id=1, producto_id=3, cantidad=2, precio_unitario=150.0),
    ]

    with patch("app.services.detalle_pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        exec_result = MagicMock()
        exec_result.all.return_value = detalles_mock
        mock_session.exec.return_value = exec_result
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = detalle_pedido_service.obtener_detalles()
        assert resultado == detalles_mock


def test_obtener_detalle_por_id():
    detalle_mock = DetallePedido(id=1, pedido_id=1, producto_id=2, cantidad=2, precio_unitario=50.0)

    with patch("app.services.detalle_pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = detalle_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = detalle_pedido_service.obtener_detalle_por_id(1)
        assert resultado == detalle_mock


def test_actualizar_detalle_exitoso():
    detalle_existente = DetallePedido(id=1, pedido_id=1, producto_id=2, cantidad=2, precio_unitario=50.0)
    datos_actualizados = DetallePedido(pedido_id=1, producto_id=2, cantidad=3, precio_unitario=60.0)

    with patch("app.services.detalle_pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = detalle_existente
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = detalle_pedido_service.actualizar_detalle(1, datos_actualizados)
        assert resultado.cantidad == 3
        assert resultado.precio_unitario == 60.0


def test_eliminar_detalle_exitoso():
    detalle_mock = DetallePedido(id=1, pedido_id=1, producto_id=2, cantidad=2, precio_unitario=50.0)

    with patch("app.services.detalle_pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = detalle_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = detalle_pedido_service.eliminar_detalle(1)
        assert resultado is True


def test_eliminar_detalle_no_existente():
    with patch("app.services.detalle_pedido_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = None
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = detalle_pedido_service.eliminar_detalle(999)
        assert resultado is False