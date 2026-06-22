from model.Nivel import Nivel, TILE_SIZE
from model.Player import Player

ancho_pantalla = 800

class GameWorld:
    def __init__(self):
        # Primero tenemos que cargar el nivel
        self.nivel = Nivel()
        self.nivel.cargar()

        # Cargamos el jugador en el SpawnPoint
        self.player = Player(self.nivel.spawn_x, self.nivel.spawn_y, False)

        # Estado del juego
        self.won = False
        self.message = None
        self.ir_castillo = False
        # Alto total del mundo (para detectar caidas)
        self.world_height = len(self.nivel.superficies) and max(
            (s.y for s in self.nivel.superficies), default=0
        )


    def _collide(self, limites_a, limites_b):
        ax, ay, aw, ah = limites_a
        bx, by, bw, bh = limites_b
        return (ax < bx + bw) and (ax + aw > bx) and (ay < by + bh) and (ay + ah > by)

    def _collide_x(self):
        p = self.player
        for surf in self.nivel.superficies:
            if self._collide(p.get_Bounds(), surf.on_Bounds()):
                if p.vx > 0:
                    # se movía a la derecha, choca → pegar a la izquierda del bloque
                    p.x = surf.x - p.player_w
                elif p.vx < 0:
                    # se movía a la izquierda, choca → pegar a la derecha del bloque
                    p.x = surf.x + surf.largo
                p.vx = 0

    def _collide_y(self):
        p = self.player
        p.isOnGround = False
        for surf in self.nivel.superficies:
            if self._collide(p.get_Bounds(), surf.on_Bounds()):
                if p.vy >= 0:
                    # cayendo → aterrizar encima del bloque
                    p.y = surf.y - p.player_h
                    p.aterrizar()
                    surf.on_collide(p)  # ← aquí se aplica el Strategy!
                elif p.vy < 0:
                    # subiendo → golpea el techo
                    p.y = surf.y + surf.ancho
                    p.vy = 0

    def update(self, actions):
        p = self.player

        # Movimiento lateral (bloqueado mientras se carga el salto, estilo Jump King)
        if p.isCharging:
            p.movimiento("")
        elif "izq" in actions:
            p.movimiento("izq")
        elif "derch" in actions:
            p.movimiento("derch")
        else:
            p.movimiento("")

        # Gestion del salto
        if ("salta") in actions:
            if p.isOnGround:
                p.cargar_salto()
        else:
            if p.isCharging:
                p.saltar()

        # Caida en picado
        if "down" in actions:
            p.caida_picado()

        # Aplicacion de la gravedad
        p.gravedad()

        # Mover en X y resolucion de colisiones horizontales
        p.x += p.vx
        self._collide_x()

        # Mover en Y y resolucion de colsiones verticales
        p.y += p.vy
        self._collide_y()

        # Comprobar monedas
        for moneda in self.nivel.moneda:
            if not moneda.cogida:
                if self._collide(p.get_Bounds(), moneda.get_Bounds()):
                    moneda.recoger()
                    p.monedas += 1
                    p.puntuacion += 10

        # Comprobar vicotiras
        meta_bounds = (self.nivel.goal_x, self.nivel.goal_y, TILE_SIZE, TILE_SIZE)
        if self._collide(p.get_Bounds(), meta_bounds):
            self.won = True
            self.message = "¡VICTORIA!"

        # Muerte por caida: si cae por debajo del mundo, vuelve al spawn
        if p.y > self.world_height + 200:
            p.x = p.spawn_x
            p.y = p.spawn_y
            p.vx = 0
            p.vy = 0
            p.muertes += 1

        # Salir de la torre, volver al castillo
        if p.x + p.player_w > ancho_pantalla:
            self.ir_castillo = True