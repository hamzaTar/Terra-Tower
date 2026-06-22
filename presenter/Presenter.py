import sys

from view.View import GameView
from view.CastilloModel import CastilloModel
from presenter.Estados import EstadoInicio


class GamePresenter:
    def __init__(self):
        self.view = GameView()
        self.castillo_model = CastilloModel()
        self.estado_actual = EstadoInicio(self)

    def cambiar_a(self, nuevo_estado):
        self.estado_actual = nuevo_estado

    def salir(self):
        self.view.close()
        sys.exit()

    def run(self):
        while True:
            siguiente = self.estado_actual.manejar_eventos()
            if siguiente:
                self.estado_actual = siguiente
                continue
            self.estado_actual.actualizar()
            self.estado_actual.dibujar()