from usuario import Usuario
from formacion import Formacion
from jugador import Jugador

PRESUPUESTO = 100_000_000

class Equipo:
    def __init__(self, usuario):
        self.usuario: Usuario = usuario
        self.valor: int = 0
        self.jugadores: list[Jugador] = []
        self.presupuesto = PRESUPUESTO - self.valor
        self.formacion: tuple[int] = Formacion.CUATRO_CUATRO_DOS # ??
        self.puntaje: int = 0
        self.historial: dict[int, int] = {} # {fecha: puntaje}
    
    def actualizar(self) -> None:
        pass

    def notificar_estado(self) -> None:
        pass

    def cambiar_formacion(self, formacion: Formacion) -> None: # no si se usa asi un enum
        self.formacion = formacion

    def agregar_jugador(self, jugador: Jugador) -> None: # hay que usar Formacion para ver si se puede agregar
        self.jugadores.append(jugador)
        self.valor += jugador.valor
        self.presupuesto -= jugador.valor

    def quitar_jugador(self, jugador: Jugador) -> None:
        self.jugadores.remove(jugador)
        self.valor -= jugador.valor
        self.presupuesto += jugador.valor
    
    def transferencia(self, jugador_entra: Jugador, jugador_sale: Jugador) -> None:
        self.quitar_jugador(jugador_sale)
        self.agregar_jugador(jugador_entra)
    