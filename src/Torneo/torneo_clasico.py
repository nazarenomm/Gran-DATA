from Torneo.torneo import Torneo
from Usuario.usuario import Usuario

class TorneoClasico(Torneo):
    def __init__(self, creador: Usuario) -> None:
        super().__init__(creador)
        