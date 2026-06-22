moneda_desbloquear_hab = 1

class CastilloModel:
    def __init__(self):
        self.monedas = 0
        self.habitaciones = [True, False, False, False, False, False]

    def anadir_monedas(self, cantidad):
        self.monedas += cantidad
        self._actualizar_desbloqueos()

    def _actualizar_desbloqueos(self):
        desbloqueadas = min(self.monedas // moneda_desbloquear_hab, 5)
        for i in range(1, 6):
            self.habitaciones[i] = (i <= desbloqueadas)
