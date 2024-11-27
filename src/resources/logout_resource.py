from flask_restx import Resource
from flask_jwt_extended import jwt_required
from extensiones import logout_ns
from flask import make_response

@logout_ns.route('')
class LogoutResource(Resource):
    @jwt_required()  # Esto asegura que el usuario esté autenticado
    def post(self):
        response = make_response({
            "message": "Logout exitoso",
            "redirect_url": "/login"  # Redirige al login después de hacer logout
        }, 200)
        
        # Aquí no eliminamos cookies ya que usas localStorage, 
        # solo enviamos un mensaje de logout exitoso
        return response