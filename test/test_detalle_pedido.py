# tests/test_detalle_pedido_service.py

from unittest.mock import MagicMock, patch

import pytest

from app.domain.entities.detalle_pedido_entity import DetallePedidoEntity
from app.services.detalle_pedido_service import DetallePedidoService


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def detalle_pedido_service(mock_session):
    with patch("app.services.detalle_pedido_service.PedidoService"):
        return DetallePedidoService(session=mock_session)



def test_crear_detalle_con_pedido_existente(detalle_pedido_service, mock_session):
    detalle_entity = DetallePedidoEntity(pedido_id=1, producto_id=2, cantidad=3, precio_unitario=10.0)

    mock_session.get.return_value = MagicMock()  # pedido existe
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    with patch("app.services.detalle_pedido_service.to_model") as to_model_mock, \
         patch("app.services.detalle_pedido_service.to_entity") as to_entity_mock:
        mock_model = MagicMock()
        to_model_mock.return_value = mock_model
        detalle_data = detalle_entity.dict()
        detalle_data["id"] = 1
        to_entity_mock.return_value = DetallePedidoEntity(**detalle_data)

        result = detalle_pedido_service.crear_detalle(detalle_entity)

    assert isinstance(result, DetallePedidoEntity)
    assert result.producto_id == 2
    mock_session.add.assert_called_with(mock_model)
    mock_session.commit.assert_called()



def test_obtener_detalles(detalle_pedido_service, mock_session):
    mock_model = MagicMock()
    mock_session.exec.return_value.all.return_value = [mock_model]

    with patch("app.services.detalle_pedido_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = DetallePedidoEntity(id=1, pedido_id=1, producto_id=1, cantidad=1, precio_unitario=50.0)

        result = detalle_pedido_service.obtener_detalles()

    assert isinstance(result, list)
    assert isinstance(result[0], DetallePedidoEntity)
    mock_session.exec.assert_called()


def test_obtener_detalle_por_id_existente(detalle_pedido_service, mock_session):
    mock_model = MagicMock()
    mock_session.get.return_value = mock_model

    with patch("app.services.detalle_pedido_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = DetallePedidoEntity(id=1, pedido_id=1, producto_id=1, cantidad=2, precio_unitario=30.0)

        result = detalle_pedido_service.obtener_detalle_por_id(1)

    assert isinstance(result, DetallePedidoEntity)
    assert result.id == 1
    mock_session.get.assert_called()


def test_obtener_detalle_por_id_inexistente(detalle_pedido_service, mock_session):
    mock_session.get.return_value = None
    result = detalle_pedido_service.obtener_detalle_por_id(999)
    assert result is None


def test_actualizar_detalle_existente(detalle_pedido_service, mock_session):
    mock_model = MagicMock()
    mock_session.get.return_value = mock_model
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    datos = DetallePedidoEntity(pedido_id=2, producto_id=5, cantidad=10, precio_unitario=15.0)

    with patch("app.services.detalle_pedido_service.to_entity") as to_entity_mock:
        detalle_data = datos.dict()
        detalle_data["id"] = 1
        to_entity_mock.return_value = DetallePedidoEntity(**detalle_data)

        result = detalle_pedido_service.actualizar_detalle(1, datos)

    assert isinstance(result, DetallePedidoEntity)
    assert result.producto_id == 5
    assert result.cantidad == 10
    mock_session.commit.assert_called()



def test_actualizar_detalle_inexistente(detalle_pedido_service, mock_session):
    mock_session.get.return_value = None
    datos = DetallePedidoEntity(pedido_id=1, producto_id=1, cantidad=1, precio_unitario=1.0)
    result = detalle_pedido_service.actualizar_detalle(999, datos)
    assert result is None


def test_eliminar_detalle_existente(detalle_pedido_service, mock_session):
    mock_detalle = MagicMock()
    mock_session.get.return_value = mock_detalle

    result = detalle_pedido_service.eliminar_detalle(1)

    assert result is True
    mock_session.delete.assert_called_with(mock_detalle)
    mock_session.commit.assert_called()


def test_eliminar_detalle_inexistente(detalle_pedido_service, mock_session):
    mock_session.get.return_value = None
    result = detalle_pedido_service.eliminar_detalle(999)
    assert result is False
