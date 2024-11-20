from extensiones import db
from werkzeug.security import generate_password_hash, check_password_hash

from services.notificador import NotificadorService

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

class EstadoModel(db.Model):
    __tablename__ = 'estados'
    estado = db.Column(db.String(100), primary_key=True)

class JugadorModel(db.Model):
    __tablename__ = 'jugadores'
    jugador_id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubes.club_id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    posicion = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(100), db.ForeignKey('estados.estado'), nullable=False)

    def cambiar_estado(self, estado):
        if self.estado != estado:
            self.estado = estado
            if self.estado in ['Lesionado', 'Suspendido', 'No Juega', 'Duda']:
                titular = RolModel.query.filter_by(rol='titular').first().rol_id
                equipos_id = [ej.equipo_id for ej in EquipoJugadorModel.query.filter_by(jugador_id=self.jugador_id, rol_id=titular).all()]
                usuarios_id = [EquipoModel.query.filter_by(equipo_id=equipo_id).first().usuario_id for equipo_id in equipos_id]
                for usuario_id in usuarios_id:
                    usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
                    NotificadorService.notificar_estado(usuario, self, estado)
            db.session.commit()

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

class RolModel(db.Model):
    __tablename__ = 'roles'
    rol_id = db.Column(db.Integer, primary_key=True)
    rol = db.Column(db.String(100), nullable=False)

class EquipoJugadorModel(db.Model):
    __tablename__ = 'equipo_jugador'
    equipo_jugador_id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipos.equipo_id'), nullable=False)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugadores.jugador_id'), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.rol_id'), nullable=False)

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
    goles_local = db.Column(db.Integer)
    goles_visitante = db.Column(db.Integer)
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

class RendimientoModel(db.Model):
    __tablename__ = 'rendimientos'
    rendimiento_id = db.Column(db.Integer, primary_key=True)
    jugador_id = db.Column(db.Integer, db.ForeignKey('jugadores.jugador_id'), nullable=False)
    partido_id = db.Column(db.Integer, db.ForeignKey('partidos.partido_id'), nullable=False)
    minutos_jugados = db.Column(db.Integer)
    goles = db.Column(db.Integer)
    asistencias = db.Column(db.Integer)
    goles_penal = db.Column(db.Integer)
    penales_ejecutados = db.Column(db.Integer)
    remates = db.Column(db.Integer)
    remates_arco = db.Column(db.Integer)
    xG = db.Column(db.Float)
    npxG = db.Column(db.Float)
    ocaciones_creadas = db.Column(db.Integer)
    goles_creados = db.Column(db.Integer)
    pases_cortos_completados = db.Column(db.Integer)
    pases_cortos_intentados = db.Column(db.Integer)
    pases_medios_completados = db.Column(db.Integer)
    pases_medios_intentados = db.Column(db.Integer)
    pases_largos_completados = db.Column(db.Integer)
    pases_largos_intentados = db.Column(db.Integer)
    xAG = db.Column(db.Float)
    xA = db.Column(db.Float)
    pases_clave = db.Column(db.Integer)
    pases_progresivos = db.Column(db.Integer)
    pases_intentados = db.Column(db.Integer)
    pases_filtrados = db.Column(db.Integer)
    centros = db.Column(db.Integer)
    corners_ejecutados = db.Column(db.Integer)
    entradas = db.Column(db.Integer)
    entradas_ganadas = db.Column(db.Integer)
    bloqueos = db.Column(db.Integer)
    remates_bloqueados = db.Column(db.Integer)
    pases_bloqueados = db.Column(db.Integer)
    intercepciones = db.Column(db.Integer)
    despejes = db.Column(db.Integer)
    errores_graves = db.Column(db.Integer)
    gambetas_intentadas = db.Column(db.Integer)
    gambetas_completadas = db.Column(db.Integer)
    traslados = db.Column(db.Integer)
    traslados_progresivos = db.Column(db.Integer)
    tarjetas_amarillas = db.Column(db.Integer)
    tarjetas_rojas = db.Column(db.Integer)
    doble_amarilla = db.Column(db.Integer)
    faltas = db.Column(db.Integer)
    faltas_ganadas = db.Column(db.Integer)
    penales_ganados = db.Column(db.Integer)
    penales_concedidos = db.Column(db.Integer)
    goles_en_contra = db.Column(db.Integer)
    recuperaciones = db.Column(db.Integer)
    duelos_aereos_ganados = db.Column(db.Integer)
    duelos_aereos_perdidos = db.Column(db.Integer)
    remates_arco_recibidos = db.Column(db.Integer)
    goles_recibidos = db.Column(db.Integer)
    atajadas = db.Column(db.Integer)
    PSxG = db.Column(db.Float)
    centros_enfrentados = db.Column(db.Float)
    centros_atajados = db.Column(db.Float)
    puntaje = db.Column(db.Integer)
    puntaje_total = db.Column(db.Integer)