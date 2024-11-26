from models import EquipoJugadorModel, EquipoModel, JugadorModel, PartidoModel, PuntajeModel, RendimientoModel, RolModel, UsuarioModel
from extensiones import db

class PuntajeService:
    @staticmethod
    def cargar_puntajes(fecha):
        usuarios_id = [usuario.usuario_id for usuario in UsuarioModel.query.all()]
        for usuario_id in usuarios_id:
            titular_id = RolModel.query.filter_by(rol='Titular').first().rol_id
            suplente_id = RolModel.query.filter_by(rol='Suplente').first().rol_id
            capitan_id = RolModel.query.filter_by(rol='Capitan').first().rol_id
            
            equipo = EquipoModel.query.filter_by(usuario_id=usuario_id).first()

            if equipo:
                equipo_id = equipo.equipo_id

                titulares_ids = [ej.jugador_id for ej in EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, rol_id=titular_id).all()]
                suplentes_ids = [ej.jugador_id for ej in EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, rol_id=suplente_id).all()]
                capitan_id = EquipoJugadorModel.query.filter_by(equipo_id=equipo_id, rol_id=capitan_id).first().jugador_id

                titulares = [JugadorModel.query.filter_by(jugador_id=jugador_id).first() for jugador_id in titulares_ids]
                suplentes = [JugadorModel.query.filter_by(jugador_id=jugador_id).first() for jugador_id in suplentes_ids]
                capitan = JugadorModel.query.filter_by(jugador_id=capitan_id).first()

                partidos_ids_fecha = [partido.partido_id for partido in PartidoModel.query.filter_by(fecha=fecha).all()]

                puntaje_total = 0
                suplentes_contados = []
                for titular in titulares:
                    # chequear si jugó
                    rendimiento = RendimientoModel.query.filter(RendimientoModel.jugador_id == titular.jugador_id, RendimientoModel.partido_id.in_(partidos_ids_fecha)).first()
                    if rendimiento:
                        puntaje_total += rendimiento.puntaje_total
                    else:
                        # si no jugó, sumar el puntaje del suplente
                        posicion = titular.posicion
                        suplente = [suplente for suplente in suplentes if suplente.posicion == posicion][0]
                        rendimiento = RendimientoModel.query.filter(RendimientoModel.jugador_id == suplente.jugador_id, RendimientoModel.partido_id.in_(partidos_ids_fecha)).first()
                        if rendimiento:
                            # si el puntaje del suplente ya se sumó no sumarlo de nuevo 
                            if suplente.jugador_id not in suplentes_contados:
                                puntaje_total += rendimiento.puntaje_total
                                suplentes_contados.append(suplente.jugador_id)


                # sumar puntaje del capitan
                rendimiento = RendimientoModel.query.filter(RendimientoModel.jugador_id == capitan.jugador_id, RendimientoModel.partido_id.in_(partidos_ids_fecha)).first()
                if rendimiento:
                    puntaje_total += rendimiento.puntaje_total
                else:
                    suplente = [suplente for suplente in suplentes if suplente.posicion == capitan.posicion][0]
                    rendimiento = RendimientoModel.query.filter(RendimientoModel.jugador_id == suplente.jugador_id, RendimientoModel.partido_id.in_(partidos_ids_fecha)).first()
                    if rendimiento:
                        if suplente.jugador_id not in suplentes_contados:
                            puntaje_total += rendimiento.puntaje_total
                            suplentes_contados.append(suplente.jugador_id)
                
                # guardar puntaje total
                puntaje = PuntajeModel(equipo_id=equipo_id, fecha=fecha, puntaje=puntaje_total)
                db.session.add(puntaje)
        db.session.commit()
