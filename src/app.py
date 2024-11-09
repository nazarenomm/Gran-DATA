from flask import Flask, render_template
from flask_restful import Api
from extensiones import db, jwt
from config import Config
from resources.usuario_resource import UsuarioResource
from resources.login_resource import LoginResource
from resources.equipo_resource import EquipoResource
from resources.torneo_resource import TorneoResource
from resources.jugador_resource import JugadorResource
from resources.menu_resource import MenuResource

app = Flask(__name__)

app.config.from_object(Config)

api = Api(app)

db.init_app(app)
jwt.init_app(app)

api.add_resource(UsuarioResource, '/usuario', '/usuario/<int:usuario_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(EquipoResource, '/equipo', '/equipo/<int:equipo_id>')
api.add_resource(TorneoResource, '/torneo', '/torneo/<int:torneo_id>')
api.add_resource(JugadorResource, '/jugador/<int:jugador_id>')
api.add_resource(MenuResource, '/menu','/menu/<int:usuario_id>')

# Rutas del Frontend
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/menu/<int:usuario_id>')
def menu(usuario_id):
    return render_template('menu.html', usuario_id=usuario_id)

if __name__ == '__main__':
    app.run(debug=True)