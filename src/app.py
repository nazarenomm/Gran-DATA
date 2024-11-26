from flask import Flask, render_template
from flask_restx import Api
from extensiones import db, jwt
from config import Config
from resources.notificacion_resource import NotificacionResource
from resources.usuario_resource import UsuarioResource
from resources.login_resource import LoginResource
from resources.equipo_resource import EquipoResource
from resources.torneo_resource import TorneoResource
from resources.jugador_resource import JugadorResource
from resources.menu_resource import MenuResource
from resources.club_resource import ClubResource
from resources.tabla_posiciones_resource import TablaPosiciones, TablaPosicionesLocal, TablaPosicionesVisitante
from resources.fixture_resource import Fixture
from resources.tablas_jugadores_resource import TablaEstadisticasPrincipales
from resources.formacion_resource import FormacionResource
from resources.puntaje_resource import PuntajeResource
from resources.veda_resource import VedaResource
from resources.prode_resource import ProdeResource

app = Flask(__name__)

app.config.from_object(Config)

api = Api(app)

db.init_app(app)
jwt.init_app(app)

api.add_resource(UsuarioResource, '/usuario', '/usuario/<int:usuario_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(EquipoResource, '/equipo/<int:equipo_id>','/equipo')
api.add_resource(TorneoResource, '/torneo', '/torneo/<int:torneo_id>')
api.add_resource(JugadorResource, '/jugadores')
api.add_resource(MenuResource,'/menu/<int:usuario_id>')
api.add_resource(TablaPosiciones, '/posiciones')
api.add_resource(TablaPosicionesLocal, '/posiciones/local')
api.add_resource(TablaPosicionesVisitante, '/posiciones/visitante')
api.add_resource(Fixture, '/fixture')
api.add_resource(TablaEstadisticasPrincipales, '/estadisticas-principales')
api.add_resource(FormacionResource, '/formaciones')
api.add_resource(ClubResource, '/api/clubes', '/api/clubes/<int:club_id>')
api.add_resource(PuntajeResource, '/puntajes', '/puntajes/<int:equipo_id>', '/puntajes/<int:equipo_id>/<int:fecha>')
api.add_resource(NotificacionResource, '/notificaciones', '/notificacion')
api.add_resource(VedaResource, '/veda')
api.add_resource(ProdeResource, '/prode/<string:fecha>', '/prode')

# Rutas del Frontend
@app.route('/home')
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

@app.route('/crear_equipo/<int:usuario_id>')
def crear_equipo(usuario_id):
    return render_template('crear_equipo.html', usuario_id=usuario_id)

@app.route('/ver_equipo/<int:equipo_id>')
def ver_equipo(equipo_id):
    return render_template('ver_equipo.html', equipo_id=equipo_id)

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/clubes')
def clubes():
    return render_template('clubes.html')

# Ruta para mostrar detalles de un club
@app.route('/clubes/<int:club_id>')
def club_detalle(club_id):
    return render_template('club_detalle.html', club_id=club_id)

if __name__ == '__main__':
    app.run(debug=True)