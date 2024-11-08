from abc import ABC, abstractmethod
from usuario.usuario import Usuario

class Torneo(ABC):
    def __init__(self, creador: Usuario) -> None:
        self.usuarios: list[Usuario] = [creador]
    
    def agregar_usuario(self, usuario: Usuario) -> None:
        self.usuarios.append(usuario)

    def quitar_usuario(self, usuario: Usuario) -> None:
        self.usuarios.remove(usuario)

    # faltan metodos abstractos