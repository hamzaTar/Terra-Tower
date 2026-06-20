from model.Player import Player
from model.Moneda import Moneda
from model.Superficies import Superficies
from model.Comportamiento import (ComportamientoNormal, ComportamientoTrampa, ComportamientoResbaladizo,
                                  ComportamientoPegajoso, ComportamientoViento, ComportamientoRebote)

TILE_SIZE = 40
HEIGHT = 600
LEVEL_MAP = [
    #  SCREEN 100 
    "XXXXXXXXXXXXXXXXXXXX",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X       G          X",
    "X      XXXX        X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                 XX",
    "X                  X",
    "X                  X",
    "X                  X",
    "X          X       X",
    "X                  X",
    "X                  X",
    "X                  X",
    "XXX                X",
    "X                  X",
    "X                  X",
    #  SCREEN 99 
    "X                  X",
    "X    XXXXXXXX      X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X              X   X",
    "X                  X",
    "X           X      X",
    "X                  X",
    "X                  X",
    "XXXX               X",
    "X                  X",
    "X                  X",
    "X           X      X",
    "X                  X",
    "X      XX          X",
    "X      XX          X",
    "XC                 X",
    "XX                 X",
    "X                  X",
    "X               XX X",
    "X            X     X",
    "X                  X",
    "XXXX               X",
    "X  C               X",
    "XXXXX         XX   X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X    XX            X",
    "X                  X",
    #  SCREEN 79 
    "X                  X",
    "X                  X",
    "XXXXXXXXXX         X",
    "XXXXXXXXX          X",
    "XXXXXXXXX          X",
    "X                 XX",
    "X                  X",
    "X XXXX             X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X       XXXXXX     X",
    "X                  X",
    "X                  X",
    "X    XXXX          X",
    "X                  X",
    #  SCREEN 69 
    "X                  X",
    "X           XXXXX  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X   XXXXX          X",
    "X                  X",
    "X                  X",
    "X   C              X",
    "X   XXX            X",
    "X                  X",
    "X             XXXX X",
    "X                  X",
    "X                  X",
    "X    XXXX          X",
    "X                  X",
    #  SCREEN 59 
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X              XXX X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X     XXXX         X",
    "X               XXXX",
    "X   WWWWWWWWWWWWWWWX",
    "X                  X",
    "X                  X",
    "X        XXXX      X",
    # SCREEN 49 another windy floor 
    "X                  X",
    "X                  X",
    "X  XX           XXXX",
    "XX                 X",
    "X                  X",
    "X                  X",
    "X          XXXXXXXXX",
    "X                  X",
    "X                  X",
    "XXX                X",
    "X   WWWWWWWWWWWWWWWX",
    "X               WWWX",
    "X             WWWWWX",
    "X           WWWWWWWX",
    "X      WWWWWWWWWWWWX",
    "X         XXXXXXXXXX",
    #  SCREEN 39 windy intro 
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X  XXXX            X",
    "X                  X",
    "X         X        X",
    "X                  X",
    "X                  X",
    "X               XX X",
    "X                  X",
    "X                  X",
    "X       XX         X",
    "X                  X",
    "X                  X",
    "X   XX             X",
    #  SCREEN 2 
    "X                  X",
    "X                  X",
    "X                  X",
    "X   XXX            X",
    "X   XXXX           X",
    "X                  X",
    "X                  X",
    "X          XXX     X",
    "X                  X",
    "X                  X",
    "X    XXX           X",
    "X                  X",
    "XX           X     X",
    "XC         XXX     X",
    "XXX                X",
    "X                  X",
    #  SCREEN 19 easy floor tut 
    "X                  X",
    "X   XX             X",
    "X                  X",
    "X           XXX    X",
    "X                  X",
    "XXXX               X",
    "X                  X",
    "X                  X",
    "X        XXXXXX    X",
    "X                  X",
    "X  XXX             X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "XXXXXXXX           X",
    #  SCREEN 9 spawn floor 
    "X                  X",
    "X              XXXXX",
    "X                  X",
    "X                  X",
    "X                  X",
    "X        XXX       X",
    "X                  X",
    "X                  X",
    "XXXX               X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X              P   X",
    "XXXXXXXXXXXXXXXXXXXX",
]

class Nivel:
    def __init__(self):
        self.superficies: list[Superficies] = []
        self.moneda: list[Moneda] = []
        self.spawn_x = 0
        self.spawn_y = 0
        self.goal_x = 0  
        self.goal_y = 0

        #self.width = width
        #self.height = height
        #self.player = Player(0, 0)

    def cargar(self):
        self.superficies = []
        self.moneda = []

        total_rows = len(LEVEL_MAP)
        y_offset = (total_rows * TILE_SIZE) - HEIGHT

        normal = ComportamientoNormal()
        viento = ComportamientoViento()


        for row_i, row in enumerate(LEVEL_MAP):
            for col_i, tile in enumerate(row):
                wx = col_i * TILE_SIZE
                wy = row_i * TILE_SIZE - y_offset

                # platforms // blocks
                if tile == 'X':
                    self.superficies.append(
                        Superficies(wx, wy, TILE_SIZE, TILE_SIZE, normal)
                    )
                # wind 
                elif tile == 'W':
                    self.superficies.append(
                        Superficies(wx, wy, TILE_SIZE, TILE_SIZE, viento)
                    )
                # coins spawn points 
                elif tile == 'C':
                    self.moneda.append(Moneda(wx, wy))
                # spawn point of player 
                elif tile == 'P':
                    self.spawn_x = wx
                    self.spawn_y = wy
                # wining zone or point
                elif tile == 'G':  
                    self.goal_x = wx
                    self.goal_y = wy

    """def _collide(self, limites_a,
                 limites_b):  # Mira si hay colision entre entidades (las distintas clases de Player, Moneda y Superficies)
        ax, ay, aw, ah = limites_a
        bx, by, bw, bh = limites_b"""

    """def update(self):
        if _collide(Player.get_Bounds(), Moneda.get_Bounds()) == True:
            pass
        if _collide(Player.get_Bounds(), Moneda.get_Bounds()) == True and Moneda.recogida == False:
            pass"""