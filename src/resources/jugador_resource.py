from flask_restx import Resource, reqparse, fields, marshal_with, abort
from models import JugadorModel

jugador_fields = {
    'jugador_id': fields.Integer,
    'club_id': fields.Integer,
    'nombre': fields.String,
    'precio': fields.Integer,
    'posicion': fields.String
}

class JugadorResource(Resource):
    @marshal_with(jugador_fields)
    def get(self, jugador_id):
        result = JugadorModel.query.filter_by(jugador_id=jugador_id).first()
        if not result:
            abort(404, message="Jugador no encontrado")
        return result