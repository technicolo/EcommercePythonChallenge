# tests/test_producto_service.py

from unittest.mock import MagicMock, patch

import pytest

from app.domain.entities.producto_entity import ProductoEntity
from app.services.producto_service import ProductoService


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def producto_service(mock_session):
    return ProductoService(session=mock_session)


def test_crear_producto(producto_service, mock_session):
    producto_entity = ProductoEntity(nombre="Fernet", precio=1500.0, stock=10)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    with patch("app.services.producto_service.to_model") as to_model_mock, \
         patch("app.services.producto_service.to_entity") as to_entity_mock:
        mock_model = MagicMock()
        to_model_mock.return_value = mock_model
        to_entity_mock.return_value = ProductoEntity(id=1, nombre="Fernet", precio=1500.0, stock=10)

        result = producto_service.crear_producto(producto_entity)

    assert isinstance(result, ProductoEntity)
    assert result.nombre == "Fernet"
    mock_session.add.assert_called_with(mock_model)
    mock_session.commit.assert_called()


def test_obtener_productos(producto_service, mock_session):
    mock_producto = MagicMock()
    mock_session.exec.return_value.all.return_value = [mock_producto]

    with patch("app.services.producto_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = ProductoEntity(id=1, nombre="Gancia", precio=1200.0, stock=5)

        result = producto_service.obtener_productos()

    assert isinstance(result, list)
    assert result[0].nombre == "Gancia"
    mock_session.exec.assert_called()


def test_obtener_producto_por_id_existente(producto_service, mock_session):
    mock_producto = MagicMock()
    mock_session.get.return_value = mock_producto

    with patch("app.services.producto_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = ProductoEntity(id=1, nombre="Sprite", precio=500.0, stock=20)

        result = producto_service.obtener_producto_por_id(1)

    assert isinstance(result, ProductoEntity)
    assert result.nombre == "Sprite"
    mock_session.get.assert_called()


def test_obtener_producto_por_id_inexistente(producto_service, mock_session):
    mock_session.get.return_value = None
    result = producto_service.obtener_producto_por_id(999)
    assert result is None


def test_actualizar_producto_existente(producto_service, mock_session):
    mock_producto = MagicMock()
    mock_session.get.return_value = mock_producto
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    datos = ProductoEntity(nombre="Pepsi", precio=600.0, stock=30)

    with patch("app.services.producto_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = ProductoEntity(id=1, nombre="Pepsi", precio=600.0, stock=30)

        result = producto_service.actualizar_producto(1, datos)

    assert isinstance(result, ProductoEntity)
    assert result.nombre == "Pepsi"
    assert result.precio == 600.0
    mock_session.commit.assert_called()


def test_actualizar_producto_inexistente(producto_service, mock_session):
    mock_session.get.return_value = None
    datos = ProductoEntity(nombre="Agua", precio=300.0, stock=100)
    result = producto_service.actualizar_producto(999, datos)
    assert result is None


def test_eliminar_producto_existente(producto_service, mock_session):
    mock_producto = MagicMock()
    mock_session.get.return_value = mock_producto

    result = producto_service.eliminar_producto(1)

    assert result is True
    mock_session.delete.assert_called_with(mock_producto)
    mock_session.commit.assert_called()


def test_eliminar_producto_inexistente(producto_service, mock_session):
    mock_session.get.return_value = None
    result = producto_service.eliminar_producto(999)
    assert result is False
