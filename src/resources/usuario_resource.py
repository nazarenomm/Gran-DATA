from flask_restx import Resource, reqparse, abort, fields, marshal_with
from models import UsuarioModel
from extensiones import db, usuario_ns

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("nombre", type=str, help="Nombre Requerido", required=True)
user_post_args.add_argument("apellido", type=str, help="Apellido Requerido", required=True)
user_post_args.add_argument('mail', type=str, help='Correo Electrónico Requerido', required=True)
user_post_args.add_argument('contraseña', type=str, help='Contraseña Requerida', required=True)
user_post_args.add_argument('telefono', type=int)

user_fields = {
    'usuario_id': fields.Integer,
    'nombre': fields.String,
    'apellido': fields.String,
    'mail': fields.String,
    'contraseña': fields.String,
    'telefono': fields.Integer
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
    
@usuario_ns.route('')
class UsuarioPostResource(Resource):
    @marshal_with(user_fields)
    @usuario_ns.expect(user_post_args)
    @usuario_ns.doc(params={'nombre': 'Nombre del usuario', 'apellido': 'Apellido del usuario', 'mail': 'Correo Electrónico del usuario', 'contraseña': 'Contraseña del usuario', 'telefono': 'Teléfono del usuario'},
                    responses={201: 'Creado', 409: 'Usuario ya registrado'})
    def post(self):
        args = user_post_args.parse_args()  # Extrae los datos de la solicitud
        if UsuarioModel.query.filter_by(mail=args['mail']).first(): # mail es unique
            return {"message": "Usuario ya registrado"}, 409
        usuario = UsuarioModel(nombre=args['nombre'], apellido=args['apellido'], mail=args['mail'],
                               telefono=args['telefono'])
        usuario.set_contraseña(args['contraseña'])
        db.session.add(usuario)
        db.session.commit()
        return usuario, 201