from flask_restx import Resource, reqparse
from extensiones import veda_service
from datetime import datetime

veda_post_args = reqparse.RequestParser()
veda_post_args.add_argument('comienzo', type=str, help='Fecha y hora de inicio de la veda')
veda_post_args.add_argument('final', type=str, help='Fecha y hora de finalización de la veda', required=True)

class VedaResource(Resource):
    def post(self):
        if veda_service.verificar_veda():
            return {'message': 'Ya estamos en veda.'}, 400
        
        args = veda_post_args.parse_args()
        if args['comienzo'] is None:
            args['comienzo'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            
        veda_service.setear_veda(args['comienzo'], args['final'])
        return {'message': 'Veda seteada correctamente.'}, 200

    def get(self):
        if veda_service.verificar_veda():
            return {'message': 'Estamos en veda.'}, 200
        else:
            return {'message': 'No estamos en veda.'}, 200

    # finaliza la veda
    def delete(self):
        veda_service.finalizar_veda()
        return {'message': 'Veda finalizada correctamente.'}, 200