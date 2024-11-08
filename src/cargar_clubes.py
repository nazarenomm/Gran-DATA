from extensiones import db
from models import ClubModel
from app import app
import pandas as pd

def cargar_club(club):
    if not ClubModel.query.filter_by(nombre=club).first():
        club_model = ClubModel(nombre=club, puntos=0,
                               partidos_jugados=0, partidos_ganados=0,
                               partidos_empatados=0, partidos_perdidos=0,
                               goles_favor=0, goles_contra=0)
        db.session.add(club_model)
    db.session.commit()

if __name__ == '__main__':
    jugadores = pd.read_csv('modelo_puntajes/data/jugadores.csv')
    clubes = jugadores['Equipo'].unique()
    with app.app_context():
        for club in clubes:
            cargar_club(club)
