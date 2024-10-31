from flask_restful import Resource, reqparse, abort
from models import UsuarioModel

login_post_args = reqparse.RequestParser()
login_post_args.add_argument('mail', type=str, help='Correo Electrónico Requerido', required=True)
login_post_args.add_argument('contraseña', type=str, help='Contraseña Requerida', required=True)

class LoginResource(Resource):
    def post(self):
        args = login_post_args.parse_args()
        usuario = UsuarioModel.query.filter_by(mail=args['mail']).first()
        if not usuario:
            abort(404, message="Usuario no registrado")
        if not usuario.verificar_contraseña(args['contraseña']):
            abort(401, message="Contraseña incorrecta")
        return {"message": "Login exitoso"}, 200