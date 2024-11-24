from flask_restx import Resource, fields, marshal_with
from flask import jsonify
from sqlalchemy import text
from extensiones import db
from models import ClubModel


club_fields = {
    'club_id': fields.Integer,
    'nombre': fields.String,
    'puntos': fields.Integer,
    'partidos_jugados': fields.Integer,
    'partidos_ganados': fields.Integer,
    'partidos_empatados': fields.Integer,
    'partidos_perdidos': fields.Integer,
    'goles_favor': fields.Integer,
    'goles_contra': fields.Integer
}

class ClubResource(Resource):
    @marshal_with(club_fields)
    def get(self, club_id=None):
        try:
            if not club_id:
                # Obtener todas las formaciones desde la base de datos
                clubes = ClubModel.query.all()
                
                # Serializar los resultados
                clubes_serializados = [
                    {"club_id": club.club_id, 
                    "nombre": club.nombre, 
                    "puntos": club.puntos, 
                    "partidos_jugados": club.partidos_jugados,
                    "partidos_ganados": club.partidos_ganados,
                    "partidos_empatados": club.partidos_empatados,
                    "partidos_perdidos": club.partidos_perdidos,
                    "goles_favor": club.goles_favor,
                    "goles_contra": club.goles_contra
                    }
                    for club in clubes]                
                return clubes_serializados, 200
            else:               
                club = ClubModel.query.filter_by(club_id=club_id).first()

                if not club:
                    return {"message": "Club no encontrado"}, 404
                
                return club, 200
        except Exception as e:
            return {"message": "Error al obtener el club", "error": str(e)}, 500