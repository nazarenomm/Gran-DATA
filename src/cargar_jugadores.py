import pandas as pd
from extensiones import db
from models import JugadorModel
from app import app

def cargar_jugador(jugador):
    if not JugadorModel.query.filter_by(nombre=jugador['Jugador'], club=jugador['Equipo']).first():
        jugador_model = JugadorModel(club=jugador['Equipo'], nombre=jugador['Jugador'],
                                     precio=jugador['Precio'], posicion=jugador['Pos'])
        db.session.add(jugador_model)
    db.session.commit()

if __name__ == '__main__':
    jugadores = pd.read_csv('modelo_puntajes/data/jugadores.csv')

    with app.app_context():
        for index, jugador in jugadores.iterrows():
            cargar_jugador(jugador)