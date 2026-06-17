from abc import ABC, abstractmethod
import random

class Comportamiento(ABC):
    @abstractmethod
    def aplicar(self, player):
        pass

class ComportamientoNormal(Comportamiento):
    def aplicar(self, player):
        pass

class ComportamientoTrampa(Comportamiento): # Ahora mismo reinicia en el (0,0) siempre.
    def aplicar(self, player):
        player.x = 0
        player.y = 0

class ComportamientoResbaladizo(Comportamiento):
    def aplicar(self, player):
        player.vx *= 0.7

class ComportamientoPejagoso(Comportamiento):
    def aplicar(self, player):
        player.vx = 0

class ComportamientoViento(Comportamiento):
    def __init__(self):
        num = random.randint(1, 2)
        valor = random.randint(1, 10)
        if num == 1:
            self.direccion = valor
        else:
            self.direccion = -valor

    def aplicar(self, player):
        player.vx += self.direccion

class ComportamientoRebote(Comportamiento):
    def aplicar(self, player):
        player.vy -= 7