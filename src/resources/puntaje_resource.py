from flask_restx import Resource, abort, fields, marshal, reqparse
from models import PuntajeModel

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
                    abort(404, message="Puntaje no encontrado")
                
                return marshal(puntaje, puntaje_fields), 200
        except Exception as e:
            return {"message": "Error al obtener el puntaje", "error": str(e)}, 500