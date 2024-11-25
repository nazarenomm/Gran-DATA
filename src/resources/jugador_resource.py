from flask_restx import Resource, reqparse, fields, marshal_with, abort
from models import JugadorModel

jugador_fields = {
    'jugador_id': fields.Integer,
    'club_id': fields.Integer,
    'nombre': fields.String,
    'precio': fields.Integer,
    'posicion': fields.String,
    'estado': fields.String
}

class JugadorResource(Resource):
    @marshal_with(jugador_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('posicion', type=str, required=True, help='La posición es obligatoria.')
        parser.add_argument('search', type=str, required=False, help='Filtro opcional por nombre o apellido.')
        args = parser.parse_args()

        posicion = args['posicion']
        search = args.get('search', '')

        query = JugadorModel.query.filter(JugadorModel.posicion == posicion)

        # Si hay un término de búsqueda, filtrar por nombre o apellido
        if search:
            query = query.filter(
                or_(
                    func.lower(JugadorModel.nombre).like(f'%{search.lower()}%'),
                    func.lower(JugadorModel.apellido).like(f'%{search.lower()}%')
                )
            )

        jugadores = query.all()

        # Convertir jugadores en un formato JSON
        return jugadores, 200