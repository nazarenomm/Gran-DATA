from flask_restx import Resource, fields, marshal_with
from extensiones import clubes_ns
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

@clubes_ns.route('/<int:club_id>')
class ClubResource(Resource):
    @clubes_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @marshal_with(club_fields)
    def get(self, club_id):
        try:          
            club = ClubModel.query.filter_by(club_id=club_id).first()

            if not club:
                return {"message": "Club no encontrado"}, 404
            
            return club, 200
        except Exception as e:
            return {"message": "Error al obtener el club", "error": str(e)}, 500

@clubes_ns.route('')
class ClubesResource(Resource):
    @clubes_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def get(self):
        try:
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
        except Exception as e:
            return {"message": "Error al obtener los clubes", "error": str(e)}, 500