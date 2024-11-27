from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import UsuarioModel, EquipoModel 
from extensiones import menu_ns

@menu_ns.route('/<int:usuario_id>')
class MenuResource(Resource):
    @menu_ns.doc(params={'usuario_id': 'El id del usuario'},
                 responses={200: 'OK', 403: 'Acceso no autorizado', 404: 'Usuario no encontrado'})
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
            "equipo_id" : equipo.equipo_id if equipo else None
        }