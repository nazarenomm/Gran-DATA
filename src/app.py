from flask import Flask
from flask_restful import Api
from db import db
from config import Config
from resources.usuario_resource import UsuarioResource

app = Flask(__name__)

app.config.from_object(Config)

api = Api(app)

db.init_app(app)

api.add_resource(UsuarioResource, '/usuario/', '/usuario/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
#     with app.app_context():
#         db.create_all()
#         user = UsuarioModel(nombre='Marcelo', apellido='Gallardo', mail='marcegalla@gmail.com', telefono=12349912)
#         user.set_password('Contraseña123')
#         user.agregar_a_db()
        
#         # Consulta todos los usuarios
#         usuarios = UsuarioModel.query.all()
#         print(usuarios)

