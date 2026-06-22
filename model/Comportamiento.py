from abc import ABC, abstractmethod
import random


class Comportamiento(ABC):
    @abstractmethod
    def aplicar(self, player):
        pass


class ComportamientoNormal(Comportamiento):
    def aplicar(self, player):
        pass


class ComportamientoTrampa(Comportamiento):
    # Devuelve al jugador a su punto de reaparicion (no a 0,0)
    def aplicar(self, player):
        player.x = player.spawn_x
        player.y = player.spawn_y
        player.vx = 0
        player.vy = 0


class ComportamientoResbaladizo(Comportamiento):
    def aplicar(self, player):
        player.vx *= 0.7


class ComportamientoPegajoso(Comportamiento):
    def aplicar(self, player):
        player.vx = 0


class ComportamientoViento(Comportamiento):
    def __init__(self):
        # Cada bloque de viento elige su propia direccion al crearse.
        # Fuerza pequena: se aplica cada frame que el jugador esta encima,
        # asi se siente como un empuje continuo, no como un lanzamiento.
        valor = random.uniform(0.4, 0.9)
        if random.randint(1, 2) == 1:
            self.direccion = valor
        else:
            self.direccion = -valor

    def aplicar(self, player):
        player.x += self.direccion


class ComportamientoRebote(Comportamiento):
    def aplicar(self, player):
        player.vy = -16
        player.isOnGround = False