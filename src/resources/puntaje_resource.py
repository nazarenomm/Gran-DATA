from flask_restx import Resource, fields, marshal_with, reqparse
from flask import jsonify
from sqlalchemy import text
from extensiones import db
from models import PuntajeModel, EquipoJugadorModel, PartidoModel, RendimientoModel


puntaje_fields = {
    'puntaje_id': fields.Integer,
    'equipo_id': fields.Integer,
    'fecha': fields.Integer,
    'puntaje': fields.Integer
}

puntaje_post_args = reqparse.RequestParser()
puntaje_post_args.add_argument('equipo_id', type=str, help='Equipo Requerido', required=True)
puntaje_post_args.add_argument('fecha', type=str, help='Fecha Requerida', required=True)

class PuntajeResource(Resource):
    @marshal_with(puntaje_fields)
    def get(self, equipo_id, fecha=None):
        try:
            if not fecha:
                # Obtener todas las formaciones desde la base de datos
                puntajes = PuntajeModel.query.filter_by(equipo_id=equipo_id).all()
                
                # Serializar los resultados
                puntajes_serializados = [
                    {"puntaje_id": puntaje.puntaje_id, 
                    "equipo_id": puntaje.equipo_id, 
                    "fecha": puntaje.fecha, 
                    "puntaje": puntaje.puntaje
                    }
                    for puntaje in puntajes]                
                return puntajes_serializados, 200
            else:               
                puntaje = PuntajeModel.query.filter_by(equipo_id=equipo_id, fecha=fecha).first()

                if not puntaje:
                    return {"message": "Puntaje no encontrado"}, 404
                
                return puntaje, 200
        except Exception as e:
            return {"message": "Error al obtener el puntaje", "error": str(e)}, 500
    

    ## No es al pedo esto?? los usuarios no van a poder crear puntajes, VA EN CARGAR_RENDIMIENTO (FUTURA CLASE FECHA)
    @marshal_with(puntaje_fields)
    def post(self):
        try:
            args = puntaje_post_args.parse_args()

            lista_id_jugadores = [ej.jugador_id for ej in EquipoJugadorModel.query.filter_by(equipo_id=args['equipo_id']).all()]
            print(lista_id_jugadores)
            partidos_id = [p.partido_id for p in PartidoModel.query.filter_by(fecha=args['fecha']).all()]
            print(partidos_id)
            puntajes_fecha = [r.puntaje_total for r in RendimientoModel.query.filter(RendimientoModel.partido_id.in_(partidos_id), RendimientoModel.jugador_id.in_(lista_id_jugadores)).all()]
            print(puntajes_fecha)

            puntaje = sum(puntajes_fecha)
            print(f'putnaje: [{puntaje}]')
            puntaje = PuntajeModel(equipo_id=args['equipo_id'], fecha=args['fecha'], puntaje=puntaje)
            db.session.add(puntaje)
            db.session.commit()
            return puntaje, 201
        except Exception as e:
            return {"message": "Error al crear el puntaje", "error": str(e)}, 500           