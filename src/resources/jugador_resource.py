from flask_restx import Resource, reqparse, fields, marshal_with, abort, reqparse
from models import JugadorModel, UsuarioModel
from extensiones import jugador_ns
from decoradores import requiere_admin
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.jugador import JugadorService

patch_args = reqparse.RequestParser()
patch_args.add_argument('precio', type=int, help='Precio del jugador')
patch_args.add_argument('estado', type=str, help='Estado del jugador')

jugador_fields = {
    'jugador_id': fields.Integer,
    'club_id': fields.Integer,
    'nombre': fields.String,
    'precio': fields.Integer,
    'posicion': fields.String,
    'estado': fields.String
}

@jugador_ns.route('')
class JugadoresResource(Resource):
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

@jugador_ns.route('/<int:jugador_id>')
class JugadorResource(Resource):
    @jwt_required()
    # @requiere_admin
    def patch(self, jugador_id):
        usuario_id = get_jwt_identity()
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()

        if not usuario:
            return {'message': 'Usuario no encontrado.'}, 404
        
        if not usuario.es_admin:
            return {'message': 'No tiene permisos para finalizar la veda.'}, 400
        
        args = patch_args.parse_args()

        if args['precio'] is None and args['estado'] is None:
            return {'message': 'No se especificó ningún campo a modificar'}, 400

        if args['precio'] is not None:
            JugadorModel.query.filter_by(jugador_id=jugador_id).update({'precio': args['precio']})
            return {'message': 'Precio actualizado correctamente'}, 200

        if args['estado'] is not None:
            jugador = JugadorModel.query.filter_by(jugador_id=jugador_id).first()
            if not jugador:
                return {'message': 'Jugador no encontrado'}, 404
            JugadorService.cambiar_estado(jugador, args['estado'])
            return {'message': 'Estado actualizado correctamente'}, 200