import pandas as pd
from extensiones import db
from models import JugadorModel, ClubModel
from app import app

def cargar_jugador(jugador):
    club = ClubModel.query.filter_by(nombre=jugador['Equipo']).first()
    club_id = club.club_id if club else None
    if not JugadorModel.query.filter_by(nombre=jugador['Jugador'], club_id=club_id).first():
        jugador_model = JugadorModel(club_id=club_id, nombre=jugador['Jugador'],
                                     precio=jugador['Precio'], posicion=jugador['Pos'], estado=jugador['Estado'],)
        db.session.add(jugador_model)
    db.session.commit()

if __name__ == '__main__':
    jugadores = pd.read_csv('modelo_puntajes/data/jugadores.csv')

    with app.app_context():
        for index, jugador in jugadores.iterrows():
            cargar_jugador(jugador)