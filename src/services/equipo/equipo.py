from models.usuario_model import UsuarioModel
from equipo.formacion import Formacion
from jugador.jugador import Jugador
from exceptions.exceptions import JugadoresMaximosException, PresupuestoInsuficienteException, JugadorNoEncontradoException

PRESUPUESTO = 100_000_000

class Equipo:
    def __init__(self, usuario):
        self.usuario: UsuarioModel = usuario
        self.valor: int = 0
        self.jugadores: list[Jugador] = [] # titulares y suplentes
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

    def check_cant_jugadores(self) -> bool:
        return len(self.jugadores) < 15
    
    def check_presupuesto(self, jugador: Jugador) -> bool:
        return self.presupuesto - jugador.valor >= 0
    
    def check_jugador(self, jugador: Jugador) -> bool:   # los checks podrían ser decoradores
        return jugador in self.jugadores
    
    def agregar_jugador(self, jugador: Jugador) -> None:
        try:
            if not self.check_cant_jugadores(): #TODO Check por posiciones
                raise JugadoresMaximosException("No se puede agregar más jugadores.")
            
            if not self.check_presupuesto(jugador):
                raise PresupuestoInsuficienteException("No tiene presupuesto suficiente.")
            
            self.jugadores.append(jugador)
            self.valor += jugador.valor
            self.presupuesto -= jugador.valor

        except (JugadoresMaximosException, PresupuestoInsuficienteException) as e:
            print(f"Error: {e}")  

    def quitar_jugador(self, jugador: Jugador) -> None:
        try:
            if not self.check_jugador(jugador):
                raise Exception("El jugador no está en el equipo.")
            self.jugadores.remove(jugador)
            self.valor -= jugador.valor
            self.presupuesto += jugador.valor
        except JugadorNoEncontradoException as e:
            print(f"Error: {e}")
    
    # Vamos a hacer transferencias de un jugador por otro o mejor primero vender y despues comprar?
    def transferencia(self, jugador_entra: Jugador, jugador_sale: Jugador) -> None: 
        self.quitar_jugador(jugador_sale)
        self.agregar_jugador(jugador_entra)
    