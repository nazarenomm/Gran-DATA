from datetime import datetime
from flask_restx import Resource, reqparse
from services import fecha, notificador

patch_args = reqparse.RequestParser()
patch_args.add_argument('comienzo', type=str, help='Fecha y hora de inicio de la veda')
patch_args.add_argument('final', type=str, help='Fecha y hora de finalización de la veda', required=True)

class FechaResource(Resource):
    # carga la fecha
    def post(self):
        fecha.cargar_fecha()
        return {'message': 'Fecha cargada correctamente'}, 200
    
    # setea la veda
    def patch(self):
        if fecha.verificar_veda():
            return {'message': 'Ya estamos en veda.'}, 400
        
        args = patch_args.parse_args()
        if args['comienzo'] is None:
            args['comienzo'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            
        fecha.setear_veda(args['comienzo'], args['final'])

        notificador.notificar_veda(args['comienzo'])

        return {'message': 'Veda seteada correctamente.'}, 200
    
    def get(self):
        if fecha.verificar_veda():
            return {'veda': 'Estamos en veda.',
                    'fecha': fecha.fecha_actual}, 200
        else:
            return {'veda': 'No estamos en veda.',
                    'fecha': fecha.fecha_actual}, 200
    
    # finaliza la veda
    def delete(self):
        fecha.finalizar_veda()
        return {'message': 'Veda finalizada correctamente.'}, 200
    
    def put(self):
        fecha.fecha_actual += 1
        return {'message': 'Fecha actualizada correctamente.'}, 200
