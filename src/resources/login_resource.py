from flask_restful import Resource, reqparse
from models import UsuarioModel
from db import db

login_post_args = reqparse.RequestParser()
login_post_args.add_argument('mail', type=str, help='Correo Electrónico Requerido', required=True)
login_post_args.add_argument('contraseña', type=str, help='Contraseña Requerida', required=True)

class LoginResource(Resource):
    def post(self):
        args = login_post_args.parse_args()
        usuario = UsuarioModel.query.filter_by(mail=args['mail']).first()
        if not usuario:
            return {"message": "Usuario no registrado"}, 404
        if not usuario.verificar_contraseña(args['contraseña']):
            return {"message": "Contraseña incorrecta"}, 401
        return {"message": "Login exitoso"}, 200