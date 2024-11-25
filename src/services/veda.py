from datetime import datetime

class VedaService:
    COMIENZO_VEDA = None
    FINAL_VEDA = None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VedaService, cls).__new__(cls, *args, **kwargs)
            cls._instance.COMIENZO_VEDA = None
            cls._instance.FINAL_VEDA = None
        return cls._instance

    def setear_veda(self, comienzo, final) -> None:
        try:
            comienzo_datetime = datetime.strptime(comienzo, '%d-%m-%Y %H:%M:%S')
            final_datetime = datetime.strptime(final, '%d-%m-%Y %H:%M:%S')

            if comienzo_datetime > final_datetime:
                raise ValueError("La fecha de comienzo de la veda no puede ser mayor a la fecha de finalización.")
            
            self.COMIENZO_VEDA = comienzo_datetime
            self.FINAL_VEDA = final_datetime

        except ValueError:
            raise ValueError("Formato de fecha/hora inválido. Usa 'YYYY-MM-DD HH:MM:SS'.")
    
    def verificar_veda(self) -> bool:
        if self.COMIENZO_VEDA is None or self.FINAL_VEDA is None:
            return False

        fecha_actual = datetime.now()
        return self.COMIENZO_VEDA <= fecha_actual <= self.FINAL_VEDA
    
    def finalizar_veda(self) -> None:
        self.COMIENZO_VEDA = None
        self.FINAL_VEDA = None