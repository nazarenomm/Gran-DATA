from flask_restful import Resource, reqparse, fields, marshal_with, abort
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
        parser = reqparse.RequestParser()
        parser.add_argument('posicion', type=str, required=True, help='La posición es obligatoria.')
        parser.add_argument('search', type=str, required=False, help='Filtro opcional por nombre o apellido.')
        args = parser.parse_args()

        posicion = args['posicion']
        search = args.get('search', '')

        query = JugadorModel.query.filter(JugadorModel.posicion == posicion)

        # Si hay un término de búsqueda, filtrar por nombre o apellido
        # if search:
        #     query = query.filter(
        #         db.or_(
        #             Jugador.nombre.ilike(f'%{search}%'),
        #             Jugador.apellido.ilike(f'%{search}%')
        #         )
        #     )

        jugadores = query.all()

        # Convertir jugadores en un formato JSON
        return [
            {
                'nombre': jugador.nombre,
                'club': jugador.club,
                'precio': jugador.precio,
                'posicion': jugador.posicion
            }
            for jugador in jugadores
        ], 200