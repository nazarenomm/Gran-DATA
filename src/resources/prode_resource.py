from flask_restx import Resource, reqparse, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import PartidoModel, ProdeModel, UsuarioModel
from extensiones import db, prode_ns
from services import fecha

post_args = reqparse.RequestParser()

post_args.add_argument("fecha", type=str, help="Fecha Requerida", required=True)
post_args.add_argument("resultados", type=list, location='json', help="Resultados Requeridos", required=True)

patch_args = reqparse.RequestParser()
patch_args.add_argument("partido_id", type=int, help="Partido ID Requerido", required=True)
patch_args.add_argument("goles_local", type=int, help="Goles Local Requerido", required=True)
patch_args.add_argument("goles_visitante", type=int, help="Goles Visitante Requerido", required=True)

# resultados = 
#     [
#      {
#       "partido_id": int,
#       "goles_local": int,
#       "goles_visitante": int
#       },
#      {...},
#     ]

@prode_ns.route('/<string:jornada>')
class ProdeResource(Resource):
    @prode_ns.doc(responses={200: 'OK', 404: 'Prodes no encontrados'}, params={'jornada': 'Fecha'})
    @jwt_required()
    def get(self, jornada):
        usuario_id = get_jwt_identity()
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
        if not usuario:
            abort(404, message="Usuario no encontrado")
            
        partidos_ids = [partido.partido_id for partido in PartidoModel.query.filter_by(fecha=jornada).all()]
        prodes = ProdeModel.query.filter(ProdeModel.usuario_id == usuario_id, ProdeModel.partido_id.in_(partidos_ids)).all()

        if not prodes:
            abort(404, message="Prodes no encontrados")
        
        prodes = [
            {
                "partido_id": prode.partido_id,
                "goles_local": prode.goles_local,
                "goles_visitante": prode.goles_visitante
            }
            for prode in prodes
        ]
        return prodes, 200
    
    @prode_ns.doc(responses={200: 'OK', 400: 'Error en la actualización', 404: 'Partido no encontrado'}, params={'fecha': 'Fecha'})
    @prode_ns.expect(patch_args)
    def patch(self, jornada):
        if fecha.verificar_veda():
            abort(400, message="Estamos en veda")
            
        args = patch_args.parse_args()
        partidos_ids_fecha = [partido.partido_id for partido in PartidoModel.query.filter_by(fecha=jornada).all()]

        if args['partido_id'] not in partidos_ids_fecha:
            abort(404, message="Partido no encontrado")
        
        prode = ProdeModel.query.filter_by(usuario_id=args['usuario_id'], partido_id=args['partido_id']).first()

        if not prode:
            abort(404, message="Prode no encontrado")

        prode.goles_local = args['goles_local']
        prode.goles_visitante = args['goles_visitante']
        db.session.commit()
        return {"message": "Prode actualizado"}, 200
    
@prode_ns.route('')
class ProdePostResource(Resource):
    @prode_ns.doc(responses={201: 'Creado', 400: 'Error en la creación', 404: 'Partido no encontrado'})
    @prode_ns.expect(post_args)
    @jwt_required()
    def post(self):
        if fecha.verificar_veda():
            abort(400, message="Estamos en veda")

        usuario_id = get_jwt_identity()
        args = post_args.parse_args()
        
        if len(args['resultados']) != 14:
            abort(400, message="Se deben ingresar 14 resultados, ingresaste {}".format(len(args['resultados'])))

        partidos_ids_fecha = [partido.partido_id for partido in PartidoModel.query.filter_by(fecha=args['fecha']).all()]

        for resultado in args['resultados']:
            if resultado['partido_id'] not in partidos_ids_fecha:
                abort(404, message="Partido no encontrado")
        
        for resultado in args['resultados']:
            prode = ProdeModel(
                usuario_id=usuario_id,
                partido_id=resultado['partido_id'],
                goles_local=resultado['goles_local'],
                goles_visitante=resultado['goles_visitante']
            )
            db.session.add(prode)
        
        db.session.commit()
        return {"message": "Prode creado"}, 201