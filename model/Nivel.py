from model.Player import Player
from model.Monedas import Moneda
from model.Superficies import Superficies
from model.Comportamiento import (ComportamientoNormal, ComportamientoTrampa, ComportamientoResbaladizo,
                                  ComportamientoPegajoso, ComportamientoViento, ComportamientoRebote)


class Nivel:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(0, 0)
        self.monedas = [Moneda(30, 70),
                        Moneda(100, 80),
                        Moneda(250, 90),
                        Moneda(75, 100),
                        Moneda(60, 150),
                        Moneda(30, 200)]
        self.superficies = [Superficies(30, 60, 80, 80, ComportamientoNormal()),
                            Superficies(100, 70, 80, 80, ComportamientoNormal()),
                            Superficies(250, 80, 80, 80, ComportamientoTrampa()),
                            Superficies(60, 170, 80, 80, ComportamientoRebote()),
                            Superficies(30, 300, 80, 80, ComportamientoViento())]

    def _collide(self, limites_a, limites_b): # Mira si hay colision entre entidades (las distintas clases de Player, Monedas y Superficies)
        ax, ay, aw, ah = limites_a
        bx, by, bw, bh = limites_b
        

    def update(self):
        if _collide(Player.get_Bounds(), Moneda.get_Bounds()) == True:
            pass
        if _collide(Player.get_Bounds(), Monedas.get_Bounds()) == True and Moneda.recogida == False:
            pass