from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(256), unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    contraseña = db.Column(db.String(128), nullable=False)
    telefono = db.Column(db.Integer, unique=True)

    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña): 
        return check_password_hash(self.contraseña, contraseña)
    
    def agregar_a_db(self):
        db.session.add(self)
        db.session.commit()

if __name__ == '__main__':
    user = User(nombre='Juan', apellido='Perez', mail ='juanperes@gmail.com', telefono=12345678)
    user.set_password('1234')
    user.agregar_a_db()

    usuarios = User.query.all()