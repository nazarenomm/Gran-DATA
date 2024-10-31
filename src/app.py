from flask import Flask
from flask_restful import Api
from db import db
from config import Config
from resources.usuario_resource import UsuarioResource
from resources.login_resource import LoginResource

app = Flask(__name__)

app.config.from_object(Config)

api = Api(app)

db.init_app(app)

api.add_resource(UsuarioResource, '/usuario/', '/usuario/<int:usuario_id>')
api.add_resource(LoginResource, '/login')

if __name__ == '__main__':
    app.run(debug=True)