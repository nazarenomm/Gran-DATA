from datetime import datetime
from models import NotificacionModel
from extensiones import db


class NotificadorService:
    @staticmethod
    def notificar_no_juega(usuario, jugador, estado):
        notificacion = NotificacionModel(
            usuario_id=usuario.usuario_id,
            titulo='Un jugador no juega',
            mensaje=f'{jugador.nombre} no jugaría en la próxima fecha, hacé cambios\nEstado: {estado}',
            fecha=datetime.now(),
            leida=False)
        db.session.add(notificacion)
        db.session.commit()

    @staticmethod
    def notificar_en_duda(usuario, jugador):
        notificacion = NotificacionModel(
            usuario_id=usuario.usuario_id,
            titulo='Un jugador está en duda',
            mensaje=f'{jugador.nombre} está en duda para la próxima fecha, hacé cambios',
            fecha=datetime.now(),
            leida=False)
        db.session.add(notificacion)
        db.session.commit()