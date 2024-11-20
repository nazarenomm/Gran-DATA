from models import JugadorModel
from extensiones import db
from app import app

def cambiar_estado(jugador_id, estado):
    jugador = JugadorModel.query.filter_by(jugador_id=jugador_id).first()
    if jugador:
        jugador.cambiar_estado(estado)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        cambiar_estado(40, 'No Juega')