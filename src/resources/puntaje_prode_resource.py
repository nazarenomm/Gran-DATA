from flask_restx import Resource, fields, abort
from extensiones import db
from models import PuntajeProdeModel

puntaje_prode_fields = {
    'puntaje_id': fields.Integer,
    'usuario_id': fields.Integer,
    'fecha': fields.Integer,
    'puntaje': fields.Integer
}

class PuntajeProdeResource(Resource):
    def get(self, usuario_id, fecha):
        puntaje = PuntajeProdeModel.query.filter_by(usuario_id=usuario_id, fecha=fecha).first()

        if not puntaje:
            abort(404, message="Puntaje no encontrado")
        
        return puntaje, 200