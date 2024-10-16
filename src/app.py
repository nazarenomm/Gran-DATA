from flask import Flask
from flask_restful import Api, Resource
from db import db
from usuario import User

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Odisea123@localhost:3306/gran_data_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class HelloWorld(Resource):
    def get(self):
        return 'Hello, World!'

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        user = User(nombre='Maria', apellido='Mernes', mail='mmernes@gmail.com', telefono=23123213)
        user.set_password('hola')
        user.agregar_a_db()
        
        # Consulta todos los usuarios
        usuarios = User.query.all()
        print(usuarios)

