from services.notificador import NotificadorService
from models import RolModel, EquipoJugadorModel, EquipoModel, UsuarioModel
from extensiones import db

class JugadorService:
    @staticmethod
    def cambiar_estado(jugador, estado):
        if jugador.estado != estado:
            jugador.estado = estado

            if jugador.estado in ['Lesionado', 'Suspendido', 'No Juega', 'Habilitado']:
                titular = RolModel.query.filter_by(rol='titular').first().rol_id
                capitan = RolModel.query.filter_by(rol='capitan').first().rol_id
                for rol in [titular, capitan]:
                    equipos_id = [ej.equipo_id for ej in EquipoJugadorModel.query.filter_by(jugador_id=jugador.jugador_id, rol_id=rol).all()]
                    if equipos_id:
                        break
                usuarios_id = [EquipoModel.query.filter_by(equipo_id=equipo_id).first().usuario_id for equipo_id in equipos_id]
                for usuario_id in usuarios_id:
                    usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
                    NotificadorService.notificar_no_juega(usuario, jugador, estado)

            if jugador.estado == 'En Duda':
                titular = RolModel.query.filter_by(rol='titular').first().rol_id
                capitan = RolModel.query.filter_by(rol='capitan').first().rol_id
                for rol in [titular, capitan]:
                    equipos_id = [ej.equipo_id for ej in EquipoJugadorModel.query.filter_by(jugador_id=jugador.jugador_id, rol_id=rol).all()]
                    if equipos_id:
                        break
                usuarios_id = [EquipoModel.query.filter_by(equipo_id=equipo_id).first().usuario_id for equipo_id in equipos_id]
                for usuario_id in usuarios_id:
                    usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
                    NotificadorService.notificar_en_duda(usuario, jugador)

            db.session.commit()

