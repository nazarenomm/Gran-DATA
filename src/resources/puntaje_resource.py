from flask_restx import Resource, abort, fields, marshal_with
from models import PuntajeModel
from extensiones import puntajes_ns

puntaje_fields = {
    'puntaje_id': fields.Integer,
    'equipo_id': fields.Integer,
    'fecha': fields.Integer,
    'puntaje': fields.Integer
}
@puntajes_ns.route('/<int:equipo_id>/<int:fecha>')
class PuntajeResource(Resource):
    @marshal_with(puntaje_fields)
    def get(self, equipo_id, fecha):
        try:
            puntaje = PuntajeModel.query.filter_by(equipo_id=equipo_id, fecha=fecha).first()

            if not puntaje:
                abort(404, message="Puntaje no encontrado")
            
            return puntaje, 200
        except Exception as e:
            return {"message": "Error al obtener el puntaje", "error": str(e)}, 500
        
@puntajes_ns.route('/<int:equipo_id>')
class PuntajeTotalResource(Resource):
    def get(self, equipo_id):
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