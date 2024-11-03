from extensiones import db
from models import FormacionModel
from app import app

def agregar_formacion(formacion: str) -> None:
    lista_formacion = formacion.split('-')
    if not len(lista_formacion) == 3:
        raise ValueError('La formación debe tener 3 números separados por guiones')
    if not FormacionModel.query.filter_by(formacion=formacion).first():
        formacion_model = FormacionModel(formacion=formacion, defensores=int(lista_formacion[0]),
                                   mediocampistas=int(lista_formacion[1]), delanteros=int(lista_formacion[2]))
        db.session.add(formacion_model)
    db.session.commit()

if __name__ == '__main__':
    formaciones = ['4-4-2', '4-3-3', '3-4-3', '4-5-1', '3-5-2', '5-3-2', '3-3-4', '4-2-4', '5-2-3']
    with app.app_context():
        for formacion in formaciones:
            agregar_formacion(formacion)