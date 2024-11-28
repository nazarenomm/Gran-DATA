from abc import ABC, abstractmethod

from models import RolesUsuarioModel, UsuarioModel
from extensiones import db

class UsuarioCreador(ABC):
    @abstractmethod
    def crear_usuario(self, nombre, apellido, mail, contraseña, telefono):
        pass

class UsuarioComunCreador(UsuarioCreador):
    def crear_usuario(self, nombre, apellido, mail, contraseña, telefono):
        rol_usuario = RolesUsuarioModel.query.filter_by(nombre="Usuario").first()
        
        usuario = UsuarioModel(nombre=nombre, apellido=apellido, mail=mail,
                               telefono=telefono, rol_id=rol_usuario.rol_id)
        usuario.set_contraseña(contraseña)

        db.session.add(usuario)
        db.session.commit()
        return usuario

class UsuarioAdminCreador(UsuarioCreador):
    def crear_usuario(self, nombre, apellido, mail, contraseña, telefono):
        rol_usuario = RolesUsuarioModel.query.filter_by(nombre="Admin").first()
        
        usuario = UsuarioModel(nombre=nombre, apellido=apellido, mail=mail,
                               telefono=telefono, rol_id=rol_usuario.rol_id)
        usuario.set_contraseña(contraseña)

        db.session.add(usuario)
        db.session.commit()
        return usuario