from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3308/gran_data_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class HelloWorld(Resource):
    def get(self):
        return 'Hello, World!'

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
