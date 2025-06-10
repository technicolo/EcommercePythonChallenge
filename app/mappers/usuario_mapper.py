# app/mappers/usuario_mapper.py

from app.domain.entities.usuario_entity import UsuarioEntity
from app.models.usuario import Usuario


def to_entity(model: Usuario) -> UsuarioEntity:
    return UsuarioEntity(id=model.id, nombre=model.nombre, email=model.email)

def to_model(entity: UsuarioEntity) -> Usuario:
    return Usuario(id=entity.id, nombre=entity.nombre, email=entity.email)
