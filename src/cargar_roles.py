from extensiones import db
from models import RolModel
from app import app

def cargar_roles():
    roles = ['titular', 'suplente', 'capitan']
    for rol in roles:
        if not RolModel.query.filter_by(rol=rol).first():
            rol_model = RolModel(rol=rol)
            db.session.add(rol_model)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        cargar_roles()