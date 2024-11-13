from flask_restx import Resource
from flask import jsonify
from sqlalchemy import text
from extensiones import db

class TablaPosiciones(Resource):
    def get(self):
        query = text('''
            WITH tabla AS (
                SELECT
                    equipo_id,
                    COUNT(*) AS partidos_jugados,
                    SUM(victorias) AS ganados,
                    SUM(empates) AS empates,
                    SUM(derrotas) AS perdidos,
                    SUM(puntos) AS puntos,
                    SUM(goles_favor) AS goles_favor,
                    SUM(goles_contra) AS goles_contra,
                    SUM(goles_favor) - SUM(goles_contra) AS diferencia_goles
                FROM (
                    -- Estadísticas para los equipos locales, excluyendo partidos futuros
                    SELECT
                        local_id AS equipo_id,
                        1 AS partidos_jugados,
                        CASE WHEN goles_local > goles_visitante THEN 1 ELSE 0 END AS victorias,
                        CASE WHEN goles_local = goles_visitante THEN 1 ELSE 0 END AS empates,
                        CASE WHEN goles_local < goles_visitante THEN 1 ELSE 0 END AS derrotas,
                        CASE WHEN goles_local > goles_visitante THEN 3
                            WHEN goles_local = goles_visitante THEN 1
                            ELSE 0
                        END AS puntos,
                        goles_local AS goles_favor,
                        goles_visitante AS goles_contra
                    FROM partidos
                    WHERE goles_local IS NOT NULL AND goles_visitante IS NOT NULL
                    UNION ALL
                    -- Estadísticas para los equipos visitantes, excluyendo partidos futuros
                    SELECT
                        visitante_id AS equipo_id,
                        1 AS partidos_jugados,
                        CASE WHEN goles_visitante > goles_local THEN 1 ELSE 0 END AS victorias,
                        CASE WHEN goles_visitante = goles_local THEN 1 ELSE 0 END AS empates,
                        CASE WHEN goles_visitante < goles_local THEN 1 ELSE 0 END AS derrotas,
                        CASE WHEN goles_visitante > goles_local THEN 3
                            WHEN goles_visitante = goles_local THEN 1
                            ELSE 0
                        END AS puntos,
                        goles_visitante AS goles_favor,
                        goles_local AS goles_contra
                    FROM partidos
                    WHERE goles_local IS NOT NULL AND goles_visitante IS NOT NULL
                ) AS estadisticas
                GROUP BY equipo_id
            )
            SELECT
                c.nombre AS equipo,
                t.puntos,
                t.partidos_jugados,
                t.ganados,
                t.empates AS empatados,
                t.perdidos,
                t.goles_favor,
                t.goles_contra,
                t.diferencia_goles
            FROM tabla AS t
            JOIN clubes AS c ON t.equipo_id = c.club_id
            ORDER BY t.puntos DESC, t.diferencia_goles DESC, t.goles_favor DESC;
        ''')

        result = db.session.execute(query).fetchall()

        # Convertir cada fila a un diccionario manualmente
        posiciones = [
            {
                "equipo": row.equipo,
                "puntos": row.puntos,
                "partidos_jugados": row.partidos_jugados,
                "ganados": row.ganados,
                "empatados": row.empatados,
                "perdidos": row.perdidos,
                "goles_favor": row.goles_favor,
                "goles_contra": row.goles_contra,
                "diferencia_goles": row.diferencia_goles,
            }
            for row in result
        ]

        return jsonify(posiciones)
    

class TablaPosicionesLocal(Resource):
    def get(self):
        query = text('''
            WITH tabla AS (
                SELECT
                    equipo_id,
                    COUNT(*) AS partidos_jugados,
                    SUM(victorias) AS ganados,
                    SUM(empates) AS empates,
                    SUM(derrotas) AS perdidos,
                    SUM(puntos) AS puntos,
                    SUM(goles_favor) AS goles_favor,
                    SUM(goles_contra) AS goles_contra,
                    SUM(goles_favor) - SUM(goles_contra) AS diferencia_goles
                FROM (
                    -- Estadísticas para los equipos locales
                    SELECT
                        local_id AS equipo_id,
                        1 AS partidos_jugados,
                        CASE WHEN goles_local > goles_visitante THEN 1 ELSE 0 END AS victorias,
                        CASE WHEN goles_local = goles_visitante THEN 1 ELSE 0 END AS empates,
                        CASE WHEN goles_local < goles_visitante THEN 1 ELSE 0 END AS derrotas,
                        CASE WHEN goles_local > goles_visitante THEN 3
                             WHEN goles_local = goles_visitante THEN 1
                             ELSE 0
                        END AS puntos,
                        goles_local AS goles_favor,
                        goles_visitante AS goles_contra
                    FROM partidos
                    WHERE goles_local IS NOT NULL AND goles_visitante IS NOT NULL
                ) AS estadisticas
                GROUP BY equipo_id
            )
            SELECT
                c.nombre AS equipo,
                t.puntos,
                t.partidos_jugados,
                t.ganados,
                t.empates AS empatados,
                t.perdidos,
                t.goles_favor,
                t.goles_contra,
                t.diferencia_goles
            FROM tabla AS t
            JOIN clubes AS c ON t.equipo_id = c.club_id
            ORDER BY t.puntos DESC, t.diferencia_goles DESC, t.goles_favor DESC;
        ''')

        result = db.session.execute(query).fetchall()

        # Convertir cada fila a un diccionario manualmente
        posiciones = [
            {
                "equipo": row.equipo,
                "puntos": row.puntos,
                "partidos_jugados": row.partidos_jugados,
                "ganados": row.ganados,
                "empatados": row.empatados,
                "perdidos": row.perdidos,
                "goles_favor": row.goles_favor,
                "goles_contra": row.goles_contra,
                "diferencia_goles": row.diferencia_goles,
            }
            for row in result
        ]

        return jsonify(posiciones)

class TablaPosicionesVisitante(Resource):
    def get(self):
        query = text('''
            WITH tabla AS (
                SELECT
                    equipo_id,
                    COUNT(*) AS partidos_jugados,
                    SUM(victorias) AS ganados,
                    SUM(empates) AS empates,
                    SUM(derrotas) AS perdidos,
                    SUM(puntos) AS puntos,
                    SUM(goles_favor) AS goles_favor,
                    SUM(goles_contra) AS goles_contra,
                    SUM(goles_favor) - SUM(goles_contra) AS diferencia_goles
                FROM (
                    -- Estadísticas para los equipos visitantes
                    SELECT
                        visitante_id AS equipo_id,
                        1 AS partidos_jugados,
                        CASE WHEN goles_visitante > goles_local THEN 1 ELSE 0 END AS victorias,
                        CASE WHEN goles_visitante = goles_local THEN 1 ELSE 0 END AS empates,
                        CASE WHEN goles_visitante < goles_local THEN 1 ELSE 0 END AS derrotas,
                        CASE WHEN goles_visitante > goles_local THEN 3
                             WHEN goles_visitante = goles_local THEN 1
                             ELSE 0
                        END AS puntos,
                        goles_visitante AS goles_favor,
                        goles_local AS goles_contra
                    FROM partidos
                    WHERE goles_local IS NOT NULL AND goles_visitante IS NOT NULL
                ) AS estadisticas
                GROUP BY equipo_id
            )
            SELECT
                c.nombre AS equipo,
                t.puntos,
                t.partidos_jugados,
                t.ganados,
                t.empates AS empatados,
                t.perdidos,
                t.goles_favor,
                t.goles_contra,
                t.diferencia_goles
            FROM tabla AS t
            JOIN clubes AS c ON t.equipo_id = c.club_id
            ORDER BY t.puntos DESC, t.diferencia_goles DESC, t.goles_favor DESC;
        ''')

        result = db.session.execute(query).fetchall()

        # Convertir cada fila a un diccionario manualmente
        posiciones = [
            {
                "equipo": row.equipo,
                "puntos": row.puntos,
                "partidos_jugados": row.partidos_jugados,
                "ganados": row.ganados,
                "empatados": row.empatados,
                "perdidos": row.perdidos,
                "goles_favor": row.goles_favor,
                "goles_contra": row.goles_contra,
                "diferencia_goles": row.diferencia_goles,
            }
            for row in result
        ]

        return jsonify(posiciones)
