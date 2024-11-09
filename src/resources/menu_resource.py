from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import UsuarioModel, EquipoModel 

class MenuResource(Resource):
    @jwt_required()
    def post(self, usuario_id):
        print("Entro al Menu########################################")
        current_user_id = get_jwt_identity()
        print(f'Current usuario id :{current_user_id}')
        print(f'Usuario id :{usuario_id}')
        if current_user_id != usuario_id:
            return {"message": "Acceso no autorizado"}, 403

        usuario = UsuarioModel.query.get(usuario_id)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404

        equipo = EquipoModel.query.filter_by(usuario_id=usuario_id).first()
        print(f'Equipo: {equipo}')
        return {
            "usuario_nombre": usuario.nombre,
            "equipo": equipo.nombre if equipo else None
        }