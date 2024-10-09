from enum import Enum

class Formacion(Enum):
    CUATRO_CUATRO_DOS = (2,2,2)
    CUATRO_TRES_TRES = (4,3,3)
    CINCO_TRES_DOS = (5,3,2)
    # ETC. Quizás usar dict en lugar de tuple si tenemos más posiciones
    # CUATRO_CUATRO_DOS = {"centrales": 2, "laterales": 2, "centrocampistas": 2, "extremos": 2, "delanteros": 2}