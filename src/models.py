from app import app, db
from services.puntaje.calificador import Calificador
from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'

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

class PuntajeModel(db.Model):
    __tablename__ = 'puntajes'
    id = db.Column(db.Integer, primary_key=True)
    jugador = db.Column(db.String(100), nullable=False)
    equipo = db.Column(db.String(30), nullable=False)
    puntaje = db.Column(db.Float)
    fecha = db.Column(db.Integer, nullable=False)

if __name__ == '__main__':
    modelo = Calificador()
    # df_fecha = modelo.computar_fecha(1)
    
    import pandas as pd
    df_fecha = pd.read_csv('modelo_puntajes/data/predicciones/predicciones_fecha_18.csv')

    with app.app_context():
        db.create_all()
        for index, row in df_fecha.iterrows():
            nuevo_puntaje = PuntajeModel(jugador=row['jugador'], equipo=row['equipo'], puntaje=row['puntaje'], fecha=row['fecha'])
            db.session.add(nuevo_puntaje) 
        db.session.commit()