from app import app
from models import JugadorModel
from services.jugador import JugadorService

def cambiar_estado(jugador_id, estado):
    jugador = JugadorModel.query.filter_by(jugador_id=jugador_id).first()
    JugadorService.cambiar_estado(jugador, estado)

if __name__ == '__main__':
    with app.app_context():
        cambiar_estado(40, 'No Juega')