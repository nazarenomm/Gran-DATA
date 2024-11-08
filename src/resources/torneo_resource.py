from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import TorneoModel, TorneoUsuarioModel, UsuarioModel
from extensiones import db
from datetime import date

torneo_post_args = reqparse.RequestParser()
torneo_post_args.add_argument("nombre", type=str, help="Nombre Requerido", required=True)
torneo_post_args.add_argument("tipo", type=str, help="Tipo de Torneo Requerido", required=True)
torneo_post_args.add_argument("creador_id", type=int, help="Creador Requerido", required=True)

torneo_put_args = reqparse.RequestParser()
torneo_put_args.add_argument("nombre", type=str)
torneo_put_args.add_argument("usuarios_id", type=int, action='append')

torneo_fields = {
    'torneo_id': fields.Integer,
    'nombre': fields.String,
    'tipo': fields.String,
    'fecha_creacion': fields.String
}

class TorneoResource(Resource):
    @marshal_with(torneo_fields)
    def get(self, torneo_id):
        torneo = TorneoModel.query.filter_by(torneo_id=torneo_id).first()
        if not torneo:
            abort(404, message="Torneo no encontrado")
        return torneo, 200
    
    @marshal_with(torneo_fields)
    def post(self):
        args = torneo_post_args.parse_args()
        creador = UsuarioModel.query.filter_by(usuario_id=args['creador_id']).first()
        if not creador:
            abort(404, message="Creador no encontrado")
        if args['tipo'] not in ['clasico', 'liga']:
            abort(400, message="Tipo de torneo no valido")
        torneo = TorneoModel(nombre=args['nombre'], tipo=args['tipo'], fecha_creacion=date.today())
        db.session.add(torneo)
        db.session.commit()
        if args['tipo'] == 'liga':
            torneo_usuario = TorneoUsuarioModel(usuario_id=args['creador_id'], torneo_id=torneo.torneo_id, es_admin=True, victorias=0, empates=0, derrotas=0)
        else:
            torneo_usuario = TorneoUsuarioModel(usuario_id=args['creador_id'], torneo_id=torneo.torneo_id, es_admin=True)
        db.session.add(torneo_usuario)
        db.session.commit()
        return torneo, 201
    
    @marshal_with(torneo_fields)
    def put(self, torneo_id):
        args = torneo_put_args.parse_args()
        torneo = TorneoModel.query.filter_by(torneo_id=torneo_id).first()
        if not torneo:
            abort(404, message="Torneo no encontrado")
        if args['nombre']:
            torneo.nombre = args['nombre']
        if args['usuarios_id']:
            for usuario_id in args['usuarios_id']:
                usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
                if not usuario:
                    abort(404, message="Usuario no encontrado")
                if TorneoUsuarioModel.query.filter_by(usuario_id=usuario_id, torneo_id=torneo.torneo_id).first():
                    abort(409, message="Usuario ya pertenece al torneo")
                if torneo.tipo == 'liga':
                    torneo_usuario = TorneoUsuarioModel(usuario_id=usuario_id, torneo_id=torneo.torneo_id, es_admin=False, victorias=0, empates=0, derrotas=0)
                else:
                    torneo_usuario = TorneoUsuarioModel(usuario_id=usuario_id, torneo_id=torneo.torneo_id, es_admin=False)
                db.session.add(torneo_usuario)
        db.session.commit()
        return torneo, 200
        
        