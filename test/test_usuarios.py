from unittest.mock import MagicMock, patch
from app.domain.usuario import Usuario
from app.services import usuario_service


def test_crear_usuario_exitoso():
    usuario_nuevo = Usuario(nombre="Juan", email="juan@example.com")
    usuario_creado = Usuario(id=1, nombre="Juan", email="juan@example.com")

    with patch("app.services.usuario_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda u: u  # simula el refresh
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = usuario_service.crear_usuario(usuario_nuevo)
        assert resultado == usuario_nuevo


def test_obtener_usuarios():
    usuarios_mock = [
        Usuario(id=1, nombre="Juan", email="juan@example.com"),
        Usuario(id=2, nombre="Ana", email="ana@example.com"),
    ]

    with patch("app.services.usuario_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        exec_result = MagicMock()
        exec_result.all.return_value = usuarios_mock
        mock_session.exec.return_value = exec_result
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = usuario_service.obtener_usuarios()
        assert resultado == usuarios_mock


def test_obtener_usuario_por_id():
    usuario_mock = Usuario(id=1, nombre="Juan", email="juan@example.com")

    with patch("app.services.usuario_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = usuario_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = usuario_service.obtener_usuario_por_id(1)
        assert resultado == usuario_mock


def test_actualizar_usuario_exitoso():
    usuario_existente = Usuario(id=1, nombre="Juan", email="viejo@example.com")
    datos_actualizados = Usuario(nombre="Juan Nuevo", email="nuevo@example.com")

    with patch("app.services.usuario_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = usuario_existente
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = usuario_service.actualizar_usuario(1, datos_actualizados)
        assert resultado.nombre == "Juan Nuevo"
        assert resultado.email == "nuevo@example.com"


def test_eliminar_usuario_exitoso():
    usuario_mock = Usuario(id=1, nombre="Juan", email="juan@example.com")

    with patch("app.services.usuario_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = usuario_mock
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = usuario_service.eliminar_usuario(1)
        assert resultado is True


def test_eliminar_usuario_no_existente():
    with patch("app.services.usuario_service.get_session") as mock_get_session:
        mock_session = MagicMock()
        mock_session.get.return_value = None
        mock_get_session.return_value.__enter__.return_value = mock_session

        resultado = usuario_service.eliminar_usuario(999)
        assert resultado is False