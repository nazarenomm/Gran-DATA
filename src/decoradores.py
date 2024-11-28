from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from models import UsuarioModel

def requiere_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Obtén el usuario_id desde el token JWT
        usuario_id = get_jwt_identity()
        
        # Verifica si el usuario existe
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404
        
        # Verifica si el usuario tiene rol de administrador
        if usuario.rol_id != 2:  # 2 es el rol de administrador
            return {"message": "Acceso denegado: Solo administradores"}, 403
        
        return func(*args, **kwargs)
    return wrapper
