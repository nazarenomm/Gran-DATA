from flask_restx import Resource, reqparse, abort, fields, marshal_with
from models import UsuarioModel, RolesUsuarioModel
from extensiones import db, usuario_ns
from services.usuario import UsuarioComunCreador, UsuarioAdminCreador

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("nombre", type=str, help="Nombre Requerido", required=True)
user_post_args.add_argument("apellido", type=str, help="Apellido Requerido", required=True)
user_post_args.add_argument('mail', type=str, help='Correo Electrónico Requerido', required=True)
user_post_args.add_argument('contraseña', type=str, help='Contraseña Requerida', required=True)
user_post_args.add_argument('telefono', type=int)

user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument('rol_id', type=int, help="ID del rol es requerido", required=True)

user_fields = {
    'usuario_id': fields.Integer,
    'nombre': fields.String,
    'apellido': fields.String,
    'mail': fields.String,
    'contraseña': fields.String,
    'telefono': fields.Integer,
    'rol_id': fields.Integer
    }

@usuario_ns.route('/<int:usuario_id>')
class UsuarioResource(Resource):
    @usuario_ns.doc(params={'usuario_id': 'ID del usuario'}, responses={200: 'OK', 404: 'Usuario no encontrado'})
    @marshal_with(user_fields)
    def get(self, usuario_id):
        result = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
        if not result:
            abort(404, message="Usuario no encontrado")
        return result
    
    @usuario_ns.doc(params={'usuario_id': 'ID del usuario'}, responses={200: 'OK', 404: 'Usuario no encontrado'})
    def delete(self, usuario_id):
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
        if not usuario:
            abort(404, message="Usuario no encontrado")
        db.session.delete(usuario)
        db.session.commit()
        return {"message": "Usuario eliminado"}, 200
    
    @usuario_ns.expect(user_patch_args)
    @usuario_ns.doc(params={'usuario_id': 'ID del usuario', 'rol_id': 'ID del rol'},
                    responses={200: 'Rol actualizado', 404: 'Usuario no encontrado', 400: 'Rol no válido'})
    def patch(self, usuario_id):
        args = user_patch_args.parse_args()  # Usa el parser definido

        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        # Verifica que el rol exista
        rol = RolesUsuarioModel.query.filter_by(rol_id=args['rol_id']).first()
        if not rol:
            return {"message": "Rol no válido"}, 400

        # Asigna el nuevo rol
        if usuario.rol_id == rol.rol_id:
            return {"message": f"El usuario ya tiene el rol {rol.nombre}"}, 400
        usuario.rol_id = rol.rol_id
        db.session.commit()
        return {"message": f"Rol actualizado a {rol.nombre}"}, 200
    
@usuario_ns.route('')
class UsuarioPostResource(Resource):
    @marshal_with(user_fields)
    @usuario_ns.expect(user_post_args)
    @usuario_ns.doc(params={'nombre': 'Nombre del usuario', 'apellido': 'Apellido del usuario', 'mail': 'Correo Electrónico del usuario', 'contraseña': 'Contraseña del usuario', 'telefono': 'Teléfono del usuario'},
                    responses={201: 'Creado', 409: 'Usuario ya registrado'})
    def post(self):
        args = user_post_args.parse_args()
        if UsuarioModel.query.filter_by(mail=args['mail']).first(): # mail es unique
            return {"message": "Usuario ya registrado"}, 409
        
        if args['rol_id'] == 1:
            creador_usuario = UsuarioComunCreador()
        elif args['rol_id'] == 2:
            creador_usuario = UsuarioAdminCreador()
        usuario = creador_usuario.crear_usuario(args['nombre'], args['apellido'], args['mail'], args['contraseña'], args['telefono'])
        return usuario, 201