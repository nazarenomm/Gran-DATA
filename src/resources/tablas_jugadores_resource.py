from flask_restx import Resource
from flask import jsonify
from sqlalchemy import text
from extensiones import db, estadisticas_principales_ns

@estadisticas_principales_ns.route('')
class TablaEstadisticasPrincipales(Resource):
    @estadisticas_principales_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    def get(self):
        query = text('''
            SELECT
	            j.nombre,
                precio,
                posicion,
                c.nombre AS equipo,
                COUNT(minutos_jugados) AS partidos_jugados,
                SUM(goles) AS goles,
                SUM(asistencias) AS asistencias,
                COUNT(goles_recibidos = 0) AS vallas_invictas,
                SUM(tarjetas_amarillas) AS tarjetas_amarillas,
                SUM(tarjetas_rojas) AS tarjetas_rojas,
                SUM(goles_penal) AS goles_penal,
                ROUND(AVG(puntaje_total), 1) AS puntaje_promedio
            FROM rendimientos r
            RIGHT JOIN jugadores j
            ON r.jugador_id = j.jugador_id
            JOIN clubes c
            ON j.club_id = c.club_id
            GROUP BY j.jugador_id
            ORDER BY goles desc;
                     '''
        )
        result = db.session.execute(query)

        tabla = [
            {
                'nombre': row.nombre,
                'precio': row.precio,
                'posicion': row.posicion,
                'equipo': row.equipo,
                'partidos_jugados': row.partidos_jugados,
                'goles': row.goles,
                'asistencias': row.asistencias,
                'vallas_invictas': row.vallas_invictas,
                'tarjetas_amarillas': row.tarjetas_amarillas,
                'tarjetas_rojas': row.tarjetas_rojas,
                'goles_penal': row.goles_penal,
                'puntaje_promedio': row.puntaje_promedio
            }
            for row in result
        ]

        return jsonify(tabla)