from config.db import db
from werkzeug.security import generate_password_hash, check_password_hash


class UsuarioModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(256), unique=True, nullable=False)
    contraseña = db.Column(db.String(256), nullable=False)
    telefono = db.Column(db.Integer, unique=True)
    
    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña): 
        return check_password_hash(self.contraseña, contraseña)
    
    def agregar_a_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.nombre} {self.apellido}>'

    