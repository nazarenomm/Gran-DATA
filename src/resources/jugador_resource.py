from flask_restx import Resource, reqparse, fields, marshal_with, abort
from models import JugadorModel
from extensiones import jugador_ns

jugador_fields = {
    'jugador_id': fields.Integer,
    'club_id': fields.Integer,
    'nombre': fields.String,
    'precio': fields.Integer,
    'posicion': fields.String,
    'estado': fields.String
}

@jugador_ns.route('')
class JugadorResource(Resource):
    @jugador_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
                    params={'posicion': 'La posición del jugador', 'search': 'Filtro opcional por nombre o apellido'})
    @marshal_with(jugador_fields)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('posicion', type=str, required=False, help='La posición es obligatoria.')
        parser.add_argument('search', type=str, required=False, help='Filtro opcional por nombre o apellido.')
        args = parser.parse_args()

        posicion = args['posicion']
        search = args.get('search', '')

        if posicion:
            query = JugadorModel.query.filter(JugadorModel.posicion == posicion)
        else:
            query = JugadorModel.query

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