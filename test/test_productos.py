from unittest.mock import MagicMock, patch

from app.domain.producto import Producto
from app.services import producto_service


def test_crear_producto_exitoso():
    producto_nuevo = Producto(nombre="Café", precio=10.0, stock=50)

    with patch("app.services.producto_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda p: p
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = producto_service.crear_producto(producto_nuevo)
        assert resultado == producto_nuevo

def test_obtener_productos():
    productos_mock = [
        Producto(id=1, nombre="Café", precio=10.0, stock=50),
        Producto(id=2, nombre="Té", precio=8.0, stock=30),
    ]

    with patch("app.services.producto_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        exec_result = MagicMock()
        exec_result.all.return_value = productos_mock
        mock_session.exec.return_value = exec_result
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = producto_service.obtener_productos()
        assert resultado == productos_mock

def test_obtener_producto_por_id():
    producto_mock = Producto(id=1, nombre="Café", precio=10.0, stock=50)

    with patch("app.services.producto_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = producto_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = producto_service.obtener_producto_por_id(1)
        assert resultado == producto_mock

def test_actualizar_producto_exitoso():
    producto_existente = Producto(id=1, nombre="Café", precio=10.0, stock=50)
    datos_actualizados = Producto(nombre="Café Premium", precio=12.5, stock=60)

    with patch("app.services.producto_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = producto_existente
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = producto_service.actualizar_producto(1, datos_actualizados)
        assert resultado.nombre == "Café Premium"
        assert resultado.precio == 12.5
        assert resultado.stock == 60

def test_eliminar_producto_exitoso():
    producto_mock = Producto(id=1, nombre="Café", precio=10.0, stock=50)

    with patch("app.services.producto_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = producto_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = producto_service.eliminar_producto(1)
        assert resultado is True

def test_eliminar_producto_no_existente():
    with patch("app.services.producto_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = None
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = producto_service.eliminar_producto(999)
        assert resultado is False
