from services.usuario import Usuario

def register_resources(api):
    api.add_resource(Usuario, '/users/<int:user_id><string:nombre><string:apellido><string:mail><string:contraseña><int:telefono>')