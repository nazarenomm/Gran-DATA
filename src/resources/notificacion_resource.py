from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, reqparse
from models import NotificacionModel
from extensiones import db

notificacion_put_args = reqparse.RequestParser()
notificacion_put_args.add_argument('notificacion_id', type=int, help='ID de la notificación', required=True)

class NotificacionResource(Resource):
    @jwt_required()
    def get(self):
        usuario_id = get_jwt_identity()
        notificaciones = NotificacionModel.query.filter_by(usuario_id=usuario_id).all()
        
        notificaciones_serializadas = [
            {
                'notificacion_id': notificacion.notificacion_id,
                'mensaje': notificacion.mensaje,
                'leida': notificacion.leida
            }
            for notificacion in notificaciones
        ]
        return notificaciones_serializadas, 200
    
    @jwt_required()
    def put(self):
        usuario_id = get_jwt_identity()
        args = notificacion_put_args.parse_args()
        if args['notificacion_id'] not in [notificacion.notificacion_id for notificacion in NotificacionModel.query.filter_by(usuario_id=usuario_id).all()]:
            return {'message': 'Notificación no encontrada'}, 404
        
        notificacion = NotificacionModel.query.filter_by(notificacion_id=args['notificacion_id']).first()
        if not notificacion:
            return {'message': 'Notificación no encontrada'}, 404
        notificacion.leida = True
        db.session.commit()
        return {'message': 'Notificación leída'}, 200
        