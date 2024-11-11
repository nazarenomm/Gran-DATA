from flask_restful import Resource
from flask import jsonify
from sqlalchemy import text
from extensiones import db

class Fixture(Resource):
    def get(self):
        query = text('''
            WITH cte AS (
	            SELECT fecha, clubes.nombre AS local, visitante_id, goles_local, goles_visitante
                FROM partidos
	            JOIN clubes ON partidos.local_id = clubes.club_id
                )
            SELECT fecha, local, goles_local, goles_visitante, clubes.nombre AS visitante
            FROM cte
            JOIN clubes ON cte.visitante_id = clubes.club_id
            ORDER BY fecha;

        ''')
        result = db.session.execute(query)

        fixture = [
            {
                'fecha': row.fecha,
                'local': row.local,
                'goles_local': row.goles_local,
                'goles_visitante': row.goles_visitante,
                'visitante': row.visitante
            }
            for row in result
        ]

        return jsonify(fixture)