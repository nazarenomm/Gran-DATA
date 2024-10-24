from abc import ABC, abstractmethod
from jugador.estado import Estado

class Jugador(ABC):
    def __init__(self, nombre: str, apellido: str, valor: int):
        self.nombre = nombre
        self.apellido = apellido
        self.valor = valor
        self.puntaje = 0
        self.estado: Estado = Estado.HABILITADO
    
    def gol(self):
        pass

    def asistencia(self):
        pass

    def amarilla(self):
        pass

    def roja(self):
        pass
