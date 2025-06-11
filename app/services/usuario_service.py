# app/services/usuario_service.py

from typing import List, Optional

from sqlmodel import Session, select

from app.domain.entities.usuario_entity import UsuarioEntity
from app.mappers.usuario_mapper import to_entity
from app.models.usuario import Usuario


class UsuarioService:
    def __init__(self, session: Session):
        self.session = session

    def obtener_usuarios(self) -> List[UsuarioEntity]:
        results = self.session.exec(select(Usuario)).all()
        return [to_entity(u) for u in results]

    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[UsuarioEntity]:
        usuario = self.session.get(Usuario, usuario_id)
        return to_entity(usuario) if usuario else None

    def actualizar_usuario(self, usuario_id: int, datos_actualizados: UsuarioEntity) -> Optional[UsuarioEntity]:
        usuario = self.session.get(Usuario, usuario_id)
        if not usuario:
            return None
        usuario.nombre = datos_actualizados.nombre
        usuario.email = datos_actualizados.email
        self.session.commit()
        self.session.refresh(usuario)
        return to_entity(usuario)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        usuario = self.session.get(Usuario, usuario_id)
        if not usuario:
            return False
        self.session.delete(usuario)
        self.session.commit()
        return True
