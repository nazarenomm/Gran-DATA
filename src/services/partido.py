class PartidoService:
    @staticmethod
    def actualizar_resultado(partido, goles_local, goles_visitante):
        partido.goles_local = goles_local
        partido.goles_visitante = goles_visitante
        return partido
            
        