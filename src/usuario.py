class Usuario:
    def __init__(self, nombre, apellido, email):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.cambios_disp = 30 # cambios para todo el torneo
    
    def comprar_cambios(self, cambios):
        self.cambios_disp += cambios