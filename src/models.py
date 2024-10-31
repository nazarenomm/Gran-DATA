from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(256), unique=True, nullable=False)
    contraseña = db.Column(db.String(256), nullable=False) # unique?
    telefono = db.Column(db.Integer, unique=True)

    def set_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

class PuntajeModel(db.Model):
    __tablename__ = 'puntajes'
    puntaje_id = db.Column(db.Integer, primary_key=True)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugadores.jugador_id'), nullable=False)
    equipo = db.Column(db.String(100), nullable=False)
    puntaje = db.Column(db.Float)
    fecha = db.Column(db.Integer, nullable=False)

class FormacionModel(db.Model):
    __tablename__ = 'formaciones'
    formacion = db.Column(db.String(100), primary_key=True)
    defensores = db.Column(db.Integer, nullable=False)
    mediocampistas = db.Column(db.Integer, nullable=False)
    delanteros = db.Column(db.Integer, nullable=False)

class EquipoModel(db.Model):
    equipo_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)
    valor = db.Column(db.Integer, nullable=False) # cotización
    formacion = db.Column(db.String(100), db.ForeignKey('formaciones.formacion'), nullable=False)

class JugadorModel(db.Model):
    