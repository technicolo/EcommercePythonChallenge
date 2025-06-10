# tests/test_usuario_service.py

from unittest.mock import MagicMock, patch

import pytest

from app.domain.entities.usuario_entity import UsuarioEntity
from app.services.usuario_service import UsuarioService


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def usuario_service(mock_session):
    return UsuarioService(session=mock_session)


def test_crear_usuario(usuario_service, mock_session):
    usuario_entity = UsuarioEntity(nombre="Juan", email="juan@mail.com")
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    with patch("app.services.usuario_service.to_model") as to_model_mock, \
         patch("app.services.usuario_service.to_entity") as to_entity_mock:
        mock_model = MagicMock()
        to_model_mock.return_value = mock_model
        to_entity_mock.return_value = UsuarioEntity(id=1, nombre="Juan", email="juan@mail.com")

        result = usuario_service.crear_usuario(usuario_entity)

    assert isinstance(result, UsuarioEntity)
    assert result.nombre == "Juan"
    mock_session.add.assert_called_with(mock_model)
    mock_session.commit.assert_called()


def test_obtener_usuarios(usuario_service, mock_session):
    mock_usuario = MagicMock()
    mock_session.exec.return_value.all.return_value = [mock_usuario]

    with patch("app.services.usuario_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = UsuarioEntity(id=1, nombre="Ana", email="ana@mail.com")

        result = usuario_service.obtener_usuarios()

    assert isinstance(result, list)
    assert result[0].nombre == "Ana"
    mock_session.exec.assert_called()


def test_obtener_usuario_por_id_existente(usuario_service, mock_session):
    mock_usuario = MagicMock()
    mock_session.get.return_value = mock_usuario

    with patch("app.services.usuario_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = UsuarioEntity(id=1, nombre="Luis", email="luis@mail.com")

        result = usuario_service.obtener_usuario_por_id(1)

    assert isinstance(result, UsuarioEntity)
    assert result.nombre == "Luis"
    mock_session.get.assert_called()


def test_obtener_usuario_por_id_inexistente(usuario_service, mock_session):
    mock_session.get.return_value = None
    result = usuario_service.obtener_usuario_por_id(999)
    assert result is None


def test_actualizar_usuario_existente(usuario_service, mock_session):
    mock_usuario = MagicMock()
    mock_session.get.return_value = mock_usuario
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    datos = UsuarioEntity(nombre="Nuevo Nombre", email="nuevo@mail.com")

    with patch("app.services.usuario_service.to_entity") as to_entity_mock:
        to_entity_mock.return_value = UsuarioEntity(id=1, nombre="Nuevo Nombre", email="nuevo@mail.com")

        result = usuario_service.actualizar_usuario(1, datos)

    assert isinstance(result, UsuarioEntity)
    assert result.nombre == "Nuevo Nombre"
    mock_session.commit.assert_called()


def test_actualizar_usuario_inexistente(usuario_service, mock_session):
    mock_session.get.return_value = None
    datos = UsuarioEntity(nombre="X", email="x@mail.com")
    result = usuario_service.actualizar_usuario(999, datos)
    assert result is None


def test_eliminar_usuario_existente(usuario_service, mock_session):
    mock_usuario = MagicMock()
    mock_session.get.return_value = mock_usuario

    result = usuario_service.eliminar_usuario(1)

    assert result is True
    mock_session.delete.assert_called_with(mock_usuario)
    mock_session.commit.assert_called()


def test_eliminar_usuario_inexistente(usuario_service, mock_session):
    mock_session.get.return_value = None
    result = usuario_service.eliminar_usuario(999)
    assert result is False
