from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app.domain.entities.pedido_entity import PedidoEntity
from app.models.detalle_pedido import DetallePedido
from app.models.pedido import PedidoCreate
from app.models.usuario import Usuario
from app.services.pedido_service import PedidoService


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def pedido_service(mock_session):
    return PedidoService(session=mock_session)


def test_crear_pedido_usuario_existente(pedido_service, mock_session):
    mock_usuario = Usuario(id=1)
    mock_session.get.return_value = mock_usuario
    mock_pedido = MagicMock(id=1, usuario_id=1, fecha=datetime.utcnow(), total=0)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    with patch("app.services.pedido_service.to_entity", return_value=PedidoEntity(id=1, usuario_id=1, fecha=mock_pedido.fecha, total=0, estado="pendiente")):
        result = pedido_service.crear_pedido(PedidoCreate(usuario_id=1))

    assert isinstance(result, PedidoEntity)
    assert result.usuario_id == 1
    mock_session.add.assert_called()


def test_obtener_pedidos(pedido_service, mock_session):
    mock_model = MagicMock()
    mock_model.usuario_id = 1
    mock_model.total = 100.0
    mock_model.fecha = datetime.utcnow()
    mock_model.id = 1
    mock_model.estado = "pendiente"  # 👈 necesario

    mock_session.exec.return_value.all.return_value = [mock_model]

    with patch(
        "app.services.pedido_service.to_entity",
        return_value=PedidoEntity(
            id=1,
            usuario_id=1,
            fecha=mock_model.fecha,
            total=100.0,
            estado=mock_model.estado  # 👈 necesario
        )
    ):
        result = pedido_service.obtener_pedidos()

    assert isinstance(result, list)
    assert isinstance(result[0], PedidoEntity)
    assert result[0].usuario_id == 1


def test_actualizar_pedido_existente(pedido_service, mock_session):
    mock_pedido = MagicMock()
    mock_pedido.usuario_id = 1
    mock_pedido.id = 1
    mock_session.get.return_value = mock_pedido
    

    with patch("app.services.pedido_service.to_entity", return_value=PedidoEntity(id=1, usuario_id=2, fecha=datetime.utcnow(), total=0, estado="pendiente")):
        result = pedido_service.actualizar_pedido(1, PedidoCreate(usuario_id=2))

    assert isinstance(result, PedidoEntity)
    assert result.usuario_id == 2
    mock_session.commit.assert_called()


def test_eliminar_pedido_existente(pedido_service, mock_session):
    mock_pedido = MagicMock()
    mock_session.get.return_value = mock_pedido

    result = pedido_service.eliminar_pedido(1)

    assert result is True
    mock_session.delete.assert_called_with(mock_pedido)
    mock_session.commit.assert_called()


def test_obtener_pedidos_por_usuario(pedido_service, mock_session):
    mock_model = MagicMock()
    mock_model.usuario_id = 1
    mock_model.total = 100.0
    mock_model.fecha = datetime.utcnow()
    mock_model.id = 1
    mock_model.estado = "pendiente" 

    mock_session.exec.return_value.all.return_value = [mock_model]

    with patch("app.services.pedido_service.to_entity", return_value=PedidoEntity(id=1, usuario_id=1, fecha=mock_model.fecha, total=100.0, estado="pendiente"  )):
        result = pedido_service.obtener_pedidos_por_usuario(1)

    assert isinstance(result, list)
    assert isinstance(result[0], PedidoEntity)
    assert result[0].usuario_id == 1


def test_actualizar_total_pedido(pedido_service, mock_session):
    mock_detalle = DetallePedido(producto_id=1, cantidad=2, precio_unitario=50.0, pedido_id=1)
    mock_session.exec.return_value.all.return_value = [mock_detalle]

    mock_pedido = MagicMock()
    mock_session.get.return_value = mock_pedido

    pedido_service.actualizar_total_pedido(1)

    assert mock_pedido.total == 100.0
    mock_session.commit.assert_called()
