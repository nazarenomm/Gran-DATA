from flask_restx import Resource, fields, abort, marshal_with
from models import PuntajeProdeModel
from extensiones import puntaje_prode_ns

puntaje_prode_fields = {
    'puntaje_id': fields.Integer,
    'usuario_id': fields.Integer,
    'fecha': fields.Integer,
    'puntaje': fields.Integer
}

@puntaje_prode_ns.route('/<int:usuario_id>/<int:fecha>')
class PuntajeProdeResource(Resource):
    @marshal_with(puntaje_prode_fields)
    def get(self, usuario_id, fecha):
    
        puntaje = PuntajeProdeModel.query.filter_by(usuario_id=usuario_id, fecha=fecha).first()

        if not puntaje:
            abort(404, message="Puntaje no encontrado")
        
        return puntaje, 200

@puntaje_prode_ns.route('/<int:usuario_id>')
class PuntajeTotalProdeResource(Resource):
    def get(self, usuario_id):
        puntajes = PuntajeProdeModel.query.filter_by(usuario_id=usuario_id).all()

        puntajes_serializados = [
            {"puntaje_id": puntaje.puntaje_id, 
            "usuario_id": puntaje.usuario_id, 
            "fecha": puntaje.fecha, 
            "puntaje": puntaje.puntaje
            }
            for puntaje in puntajes]

        return puntajes_serializados, 200