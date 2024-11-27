from datetime import datetime
from models import NotificacionModel, UsuarioModel
from extensiones import db


class NotificadorService:
    def notificar_no_juega(self, usuario, jugador, estado):
        notificacion = NotificacionModel(
            usuario_id=usuario.usuario_id,
            titulo='Un jugador no juega',
            mensaje=f'{jugador.nombre} no jugaría en la próxima fecha, hacé cambios\nEstado: {estado}',
            fecha=datetime.now(),
            leida=False)
        db.session.add(notificacion)
        db.session.commit()

    def notificar_en_duda(self, usuario, jugador):
        notificacion = NotificacionModel(
            usuario_id=usuario.usuario_id,
            titulo='Un jugador está en duda',
            mensaje=f'{jugador.nombre} está en duda para la próxima fecha, hacé cambios',
            fecha=datetime.now(),
            leida=False)
        db.session.add(notificacion)
        db.session.commit()

    def notificar_veda(self, comienzo):
        comienzo = datetime.strptime(comienzo, '%d-%m-%Y %H:%M:%S')
        if comienzo.date() == datetime.now().date():
            for usuario in UsuarioModel.query.all():
                notificacion = NotificacionModel(
                    usuario_id=usuario.usuario_id,
                    titulo='Arranca la fecha',
                    mensaje=f'La fecha comienza a las {comienzo.hour}:{comienzo.minute}, apurate a hacer tus cambios',
                    fecha=datetime.now(),
                    leida=False)
                db.session.add(notificacion)
        else:
            for usuario in UsuarioModel.query.all():
                notificacion = NotificacionModel(
                    usuario_id=usuario.usuario_id,
                    titulo='Arranca la fecha',
                    mensaje=f'La fecha comienza el {comienzo.day}/{comienzo.month} a las {comienzo.hour}:{comienzo.minute}, hacé tus cambio antes',
                    fecha=datetime.now(),
                    leida=False)
                db.session.add(notificacion)
        db.session.commit()