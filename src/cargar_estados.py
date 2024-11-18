from extensiones import db
from models import EstadoModel
from app import app

def cargar_estados():
    estados = [
        'Posible Titular',
        'Habilitado',
        'Lesionado',
        'Suspendido',
        'Duda',
        'No Juega'
    ]
    for estado in estados:
        estado_model = EstadoModel(estado=estado)
        db.session.add(estado_model)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        cargar_estados()