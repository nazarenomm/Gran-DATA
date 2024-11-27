from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, reqparse, fields, marshal_with, abort
from models import TorneoModel, TorneoUsuarioModel, UsuarioModel
from extensiones import db, torneo_ns
from datetime import date

torneo_post_args = reqparse.RequestParser()
torneo_post_args.add_argument("nombre", type=str, help="Nombre Requerido", required=True)

patch_args = reqparse.RequestParser()
patch_args.add_argument("nombre", type=str)
patch_args.add_argument("usuario_id", type=int)

torneo_fields = {
    'torneo_id': fields.Integer,
    'nombre': fields.String,
    'fecha_creacion': fields.String
}

@torneo_ns.route('/<int:torneo_id>')
class TorneoResource(Resource):
    @torneo_ns.doc(params={'torneo_id': 'ID del torneo'}, responses={200: 'OK', 404: 'Torneo no encontrado'})
    def get(self, torneo_id):
        torneo = TorneoModel.query.filter_by(torneo_id=torneo_id).first()

        if not torneo:
            abort(404, message="Torneo no encontrado")

        retorno = {}
        usuarios_id = [tu.usuario_id for tu in TorneoUsuarioModel.query.filter_by(torneo_id=torneo_id).all()]
        retorno['torneo_id'] = torneo.torneo_id
        retorno['nombre'] = torneo.nombre
        retorno['fecha_creacion'] = torneo.fecha_creacion
        retorno['usuarios_id'] = usuarios_id

        return retorno

    @torneo_ns.doc(params={'torneo_id': 'ID del Torneo'}, responses={200: 'OK', 404: 'Torneo no encontrado'})
    @torneo_ns.expect(patch_args)
    @jwt_required()
    def patch(self, torneo_id):
        args = patch_args.parse_args()
        torneo = TorneoModel.query.filter_by(torneo_id=torneo_id).first()
        if not torneo:
            abort(404, message="Torneo no encontrado")

        if args['nombre']:
            torneo.nombre = args['nombre']

        if args['usuario_id']:
            usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
            if not usuario:
                abort(404, message="Usuario no encontrado")
            if TorneoUsuarioModel.query.filter_by(usuario_id=usuario_id, torneo_id=torneo.torneo_id).first():
                abort(409, message="Usuario ya pertenece al torneo")
            torneo_usuario = TorneoUsuarioModel(usuario_id=usuario_id, torneo_id=torneo.torneo_id, es_admin=False)
            db.session.add(torneo_usuario)
        db.session.commit()
        return {"message": "torneo actualizado"}, 200

@torneo_ns.route('')
class TorneoPostResource(Resource):
    @torneo_ns.doc(responses={201: 'Creado', 400: 'Faltan datos', 401: 'No autorizado'})
    @torneo_ns.expect(torneo_post_args)
    @jwt_required()
    def post(self):
        args = torneo_post_args.parse_args()
        creador_id = get_jwt_identity()
        creador = UsuarioModel.query.filter_by(usuario_id=creador_id).first()
        if not creador:
            abort(404, message="Creador no encontrado")

        torneo = TorneoModel(nombre=args['nombre'], fecha_creacion=date.today())
        db.session.add(torneo)
        db.session.commit()

        torneo_usuario = TorneoUsuarioModel(usuario_id=creador_id, torneo_id=torneo.torneo_id, es_admin=True)

        db.session.add(torneo_usuario)
        db.session.commit()
        return {"message": "Torneo creado"}, 201
    
        