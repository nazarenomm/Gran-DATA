from Torneo.torneo import Torneo
from Usuario.usuario import Usuario

class Liga(Torneo):
    def __init__(self, creador: Usuario) -> None:
        super().__init__(creador)
        self.fixture: dict[int, list[tuple[Usuario, Usuario]]] = {}