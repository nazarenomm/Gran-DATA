from extensiones import db
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'

    usuario_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    mail = db.Column(db.String(256), unique=True, nullable=False)
    contraseña = db.Column(db.String(256), nullable=False) # unique?
    telefono = db.Column(db.Integer, unique=True)

    def set_contraseña(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

class ClubModel(db.Model):
    __tablename__ = 'clubes'
    club_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    puntos = db.Column(db.Integer, nullable=False)
    partidos_jugados = db.Column(db.Integer, nullable=False)
    partidos_ganados = db.Column(db.Integer, nullable=False)
    partidos_empatados = db.Column(db.Integer, nullable=False)
    partidos_perdidos = db.Column(db.Integer, nullable=False)
    goles_favor = db.Column(db.Integer, nullable=False)
    goles_contra = db.Column(db.Integer, nullable=False)

class JugadorModel(db.Model):
    __tablename__ = 'jugadores'
    jugador_id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubes.club_id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    posicion = db.Column(db.String(100), nullable=False)

class FormacionModel(db.Model):
    __tablename__ = 'formaciones'
    formacion = db.Column(db.String(100), primary_key=True)
    defensores = db.Column(db.Integer, nullable=False)
    mediocampistas = db.Column(db.Integer, nullable=False)
    delanteros = db.Column(db.Integer, nullable=False)

class EquipoModel(db.Model):
    __tablename__ = 'equipos'
    equipo_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)
    valor = db.Column(db.Integer, nullable=False) # cotización
    formacion = db.Column(db.String(100), db.ForeignKey('formaciones.formacion'), nullable=False)
    jugadores_id = db.Column(db.JSON, nullable=False)

class PuntajeModel(db.Model):
    __tablename__ = 'puntajes'
    puntaje_id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipos.equipo_id'), nullable=False)
    fecha = db.Column(db.Integer, nullable=False)
    puntaje = db.Column(db.Integer)

class PartidoModel(db.Model):
    __tablename__ = 'partidos'
    partido_id = db.Column(db.Integer, primary_key=True)
    local_id = db.Column(db.Integer, db.ForeignKey('clubes.club_id'), nullable=False)
    visitante_id = db.Column(db.Integer, db.ForeignKey('clubes.club_id'), nullable=False)
    goles_local = db.Column(db.Integer, nullable=False)
    goles_visitante = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Integer, nullable=False)

class TorneoModel(db.Model):
    __tablename__ = 'torneos'
    torneo_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.Date, nullable=False)

class TorneoUsuarioModel(db.Model):
    __tablename__ = 'torneo_usuario'
    torneo_usuario_id = db.Column(db.Integer, primary_key=True)
    torneo_id = db.Column(db.Integer, db.ForeignKey('torneos.torneo_id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuario_id'), nullable=False)
    es_admin = db.Column(db.Boolean, nullable=False)
    victorias = db.Column(db.Integer)
    empates = db.Column(db.Integer)
    derrotas = db.Column(db.Integer)