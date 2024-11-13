from flask import Flask, render_template
from flask_restx import Api
from extensiones import db, jwt
from config import Config
from resources.usuario_resource import UsuarioResource
from resources.login_resource import LoginResource
from resources.equipo_resource import EquipoResource
from resources.torneo_resource import TorneoResource
from resources.jugador_resource import JugadorResource
from resources.tabla_posiciones_resource import TablaPosiciones, TablaPosicionesLocal, TablaPosicionesVisitante
from resources.fixture_resource import Fixture
from resources.tablas_jugadores_resource import TablaEstadisticasPrincipales

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
api.add_resource(TablaPosiciones, '/posiciones')
api.add_resource(TablaPosicionesLocal, '/posiciones/local')
api.add_resource(TablaPosicionesVisitante, '/posiciones/visitante')
api.add_resource(Fixture, '/fixture')
api.add_resource(TablaEstadisticasPrincipales, '/estadisticas-principales')

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

if __name__ == '__main__':
    app.run(debug=True)