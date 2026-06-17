class Superficies:
    def __init__(self, x, y, largo, ancho, comportamiento):
        self.x = x
        self.y = y
        self.largo = largo
        self.ancho = ancho
        self.comportamiento = comportamiento

    def on_collide(self, player):
        self.comportamiento.aplicar(player)