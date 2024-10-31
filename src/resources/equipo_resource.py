from flask_restful import Resource, reqparse, fields, marshal_with
from models import EquipoModel
from db import db

equipo_post_args = reqparse.RequestParser()
equipo_post_args.add_argument("usuario_id", type=int, help="Usuario ID Requerido", required=True)
equipo_post_args.add_argument("valor", type=int, help="Valor Requerido", required=True)
equipo_post_args.add_argument('formacion', type=str, help='Formación Requerida', required=True)

equipo_fields = {
    'equipo_id': fields.Integer,
    'usuario_id': fields.Integer,
    'valor': fields.Integer,
    'formacion': fields.String
    }

class EquipoResource(Resource):
    @marshal_with(equipo_fields)
    def get(self, equipo_id):
        result = EquipoModel.query.filter_by(equipo_id=equipo_id).first()
        if not result:
            return {"message": "Equipo no encontrado"}, 404
        return result
    
    def delete(self, equipo_id):
        equipo = EquipoModel.query.filter_by(equipo_id=equipo_id).first()
        if not equipo:
            return {"message": "Equipo no encontrado"}, 404
        db.session.delete(equipo)
        db.session.commit()
        return {"message": "Equipo eliminado"}, 200