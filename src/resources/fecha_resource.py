from datetime import datetime
from flask_restx import Resource, reqparse
from models import UsuarioModel
from services import fecha, notificador
from extensiones import fecha_ns
from decoradores import requiere_admin
from flask_jwt_extended import get_jwt_identity, jwt_required

patch_args = reqparse.RequestParser()
patch_args.add_argument('comienzo', type=str, help='Fecha y hora de inicio de la veda')
patch_args.add_argument('final', type=str, help='Fecha y hora de finalización de la veda', required=True)

@fecha_ns.route('')
class FechaResource(Resource):
    # carga la fecha
    @fecha_ns.doc(responses={200: 'OK', 400: 'Error al cargar la fecha'})
    @jwt_required() 
    # @requiere_admin
    def post(self):
        usuario_id = get_jwt_identity()
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()

        if not usuario:
            return {'message': 'Usuario no encontrado.'}, 404
        
        if not usuario.rol_id == 2:
            return {'message': 'No tiene permisos para cargar la fecha.'}, 400
        
        # en realidad deberia terminar la veda si estamos en una
        if fecha.verificar_veda():
            return {'message': 'No se puede cargar la fecha en veda.'}, 400
        
        fecha.cargar_fecha()
        
        fecha.fecha_actual += 1

        return {'message': 'Fecha cargada correctamente'}, 200
    
    # setea la veda
    @fecha_ns.doc(responses={200: 'OK', 400: 'Ya estamos en veda'})
    @jwt_required()
    # @requiere_admin
    def patch(self):
        usuario_id = get_jwt_identity()
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()

        if not usuario:
            return {'message': 'Usuario no encontrado.'}, 404
        
        if not usuario.rol_id == 2:
            return {'message': 'No tiene permisos para setear la veda.'}, 400
        
        if fecha.verificar_veda():
            return {'message': 'Ya estamos en veda.'}, 400
        
        args = patch_args.parse_args()
        if args['comienzo'] is None:
            args['comienzo'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            
        fecha.setear_veda(args['comienzo'], args['final'])

        notificador.notificar_veda(args['comienzo'])

        return {'message': 'Veda seteada correctamente.'}, 200
    
    @fecha_ns.doc(responses={200: 'OK'})
    def get(self):
        if fecha.verificar_veda():
            return {'veda': 'Estamos en veda.',
                    'fecha': fecha.fecha_actual}, 200
        else:
            return {'veda': 'No estamos en veda.',
                    'fecha': fecha.fecha_actual}, 200
    
    # finaliza la veda
    @fecha_ns.doc(responses={200: 'OK', 400: 'No estamos en veda'})
    @jwt_required()
    # @requiere_admin
    def delete(self):
        usuario_id = get_jwt_identity()
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()

        if not usuario:
            return {'message': 'Usuario no encontrado.'}, 404

        if not usuario.rol_id == 2:
            return {'message': 'No tiene permisos para finalizar la veda.'}, 400
        
        if not fecha.verificar_veda():
            return {'message': 'No estamos en veda.'}, 400
        fecha.finalizar_veda()
        return {'message': 'Veda finalizada correctamente.'}, 200