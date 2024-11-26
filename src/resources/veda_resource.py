from flask_restx import Resource, reqparse
from services import veda, notificador
from datetime import datetime

veda_post_args = reqparse.RequestParser()
veda_post_args.add_argument('comienzo', type=str, help='Fecha y hora de inicio de la veda')
veda_post_args.add_argument('final', type=str, help='Fecha y hora de finalización de la veda', required=True)

class VedaResource(Resource):
    def post(self):
        if veda.verificar_veda():
            return {'message': 'Ya estamos en veda.'}, 400
        
        args = veda_post_args.parse_args()
        if args['comienzo'] is None:
            args['comienzo'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            
        veda.setear_veda(args['comienzo'], args['final'])

        notificador.notificar_veda(args['comienzo'])

        return {'message': 'Veda seteada correctamente.'}, 200

    def get(self):
        if veda.verificar_veda():
            return {'message': 'Estamos en veda.'}, 200
        else:
            return {'message': 'No estamos en veda.'}, 200

    # finaliza la veda
    def delete(self):
        veda.finalizar_veda()
        return {'message': 'Veda finalizada correctamente.'}, 200