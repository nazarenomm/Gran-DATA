from models import PartidoModel, ProdeModel, PuntajeProdeModel, UsuarioModel
from extensiones import db

class PuntajeProdeService:
    @staticmethod
    def cargar_puntajes(fecha):
        usuarios_id = [usuario.usuario_id for usuario in UsuarioModel.query.all()]
        partitdos_id = [partido.partido_id for partido in PartidoModel.query.filter_by(fecha=fecha).all()]
        for usuario_id in usuarios_id:
            prodes = ProdeModel.query.filter(ProdeModel.usuario_id == usuario_id, ProdeModel.partido_id.in_(partitdos_id)).all()
            if prodes:
                puntaje_total = 0
                for prode in prodes:
                    partido = PartidoModel.query.filter_by(partido_id=prode.partido_id).first()

                    prode_gano_local = prode.goles_local > prode.goles_visitante
                    prode_gano_visitante = prode.goles_local < prode.goles_visitante
                    prode_empate = prode.goles_local == prode.goles_visitante
                    partido_gano_local = partido.goles_local > partido.goles_visitante
                    partido_gano_visitante = partido.goles_local < partido.goles_visitante
                    partido_empate = partido.goles_local == partido.goles_visitante

                    if prode.goles_local == partido.goles_local and prode.goles_visitante == partido.goles_visitante:
                        puntaje_total += 3
                    elif prode_gano_local == partido_gano_local:
                        puntaje_total += 1
                    elif prode_gano_visitante == partido_gano_visitante:
                        puntaje_total += 1
                    elif prode_empate == partido_empate:
                        puntaje_total += 1
                # guardamos puntaje
                puntaje_prode = PuntajeProdeModel(usuario_id=usuario_id, fecha=fecha, puntaje=puntaje_total)
                db.session.add(puntaje_prode)
        db.session.commit()