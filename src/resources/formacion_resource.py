from flask_restx import Resource, fields, marshal_with
from flask import jsonify
from sqlalchemy import text
from extensiones import db
from models import FormacionModel


jugador_fields = {
    'formacion': fields.String,
    'defensores': fields.Integer,
    'mediocampistas': fields.Integer,
    'delanteros': fields.Integer
}

class FormacionResource(Resource):
    @marshal_with(jugador_fields)
    def get(self):
        try:
            # Obtener todas las formaciones desde la base de datos
            formaciones = FormacionModel.query.all()
            
            # Serializar los resultados
            formaciones_serializadas = [
                {"formacion": formacion.formacion, 
                 "defensores": formacion.defensores, 
                 "mediocampistas": formacion.mediocampistas, 
                 "delanteros": formacion.delanteros}
                for formacion in formaciones
            ]
            
            return formaciones_serializadas, 200
        except Exception as e:
            return {"message": "Error al obtener las formaciones", "error": str(e)}, 500

