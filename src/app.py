from flask import Flask
from flask_restful import Api, Resource
from db import db
from usuario import Usuario

app = Flask(__name__)
api = Api(app)

# db Lau
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Odisea123@localhost:3306/gran_data_test'

# db Naza 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3308/gran_data_test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class HelloWorld(Resource):
    def get(self):
        return 'Hello, World!'

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        user = Usuario(nombre='Lucas', apellido='Alexia', mail='lualexia@gmail.com', telefono=11525212)
        user.set_password('Contraseña123')
        user.agregar_a_db()
        
        # Consulta todos los usuarios
        usuarios = Usuario.query.all()
        print(usuarios)

