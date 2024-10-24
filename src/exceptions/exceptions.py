class JugadoresMaximosException(Exception):
    """Error lanzado cuando se intenta agregar más jugadores de los permitidos."""
    pass

class PresupuestoInsuficienteException(Exception):
    """Error lanzado cuando no hay presupuesto suficiente para agregar un jugador."""
    pass

class JugadorNoEncontradoException(Exception):
    """Error lanzado cuando se intenta quitar un jugador que no está en el equipo."""
    pass