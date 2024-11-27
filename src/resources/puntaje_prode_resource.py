from flask_restx import Resource, fields, abort, marshal
from models import PuntajeProdeModel

puntaje_prode_fields = {
    'puntaje_id': fields.Integer,
    'usuario_id': fields.Integer,
    'fecha': fields.Integer,
    'puntaje': fields.Integer
}

class PuntajeProdeResource(Resource):
    def get(self, usuario_id, fecha=None):
        if not fecha:
            puntajes = PuntajeProdeModel.query.filter_by(usuario_id=usuario_id).all()

            puntajes_serializados = [
                {"puntaje_id": puntaje.puntaje_id, 
                "usuario_id": puntaje.usuario_id, 
                "fecha": puntaje.fecha, 
                "puntaje": puntaje.puntaje
                }
                for puntaje in puntajes]

            return puntajes_serializados, 200
        else:
            puntaje = PuntajeProdeModel.query.filter_by(usuario_id=usuario_id, fecha=fecha).first()

            if not puntaje:
                abort(404, message="Puntaje no encontrado")
            
        return marshal(puntaje, puntaje_prode_fields), 200