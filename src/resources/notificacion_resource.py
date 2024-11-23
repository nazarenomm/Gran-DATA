from flask_restful import Resource
from models import NotificacionModel
from extensiones import db

class NotificacionResource(Resource):
    def get(self, usuario_id):
        notificaciones = NotificacionModel.query.filter_by(usuario_id=usuario_id).all()
        return [notificacion.json() for notificacion in notificaciones], 200
    
    def put(self, notificacion_id):
        notificacion = NotificacionModel.query.filter_by(notificacion_id=notificacion_id).first()
        if not notificacion:
            return {'message': 'Notificación no encontrada'}, 404
        notificacion.leida = True
        db.session.commit()
        return {'message': 'Notificación leída'}, 200
        