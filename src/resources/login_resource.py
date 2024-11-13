from flask_restx import Resource, reqparse, abort
from flask_jwt_extended import create_access_token, create_refresh_token
from models import UsuarioModel

login_post_args = reqparse.RequestParser()
login_post_args.add_argument('mail', type=str, help='Correo Electrónico Requerido', required=True)
login_post_args.add_argument('contraseña', type=str, help='Contraseña Requerida', required=True)

class LoginResource(Resource):
    def post(self):
        args = login_post_args.parse_args()
        usuario = UsuarioModel.query.filter_by(mail=args['mail']).first()  # TODO: hacer funcion "get_usuario_por_mail" para no poner query
        if not usuario:
            abort(404, message="Usuario no registrado")
        if not usuario.verificar_contraseña(args['contraseña']):
            abort(401, message="Contraseña incorrecta")
        access_token = create_access_token(identity=usuario.mail)
        refresh_token = create_refresh_token(identity=usuario.mail)
        return {
            "message": "Login exitoso",
            "access_token": access_token,
            "refresh_token": refresh_token
            }, 200