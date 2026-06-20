class Superficies:
    def __init__(self, x, y, largo, ancho, comportamiento):
        self.x = x
        self.y = y
        self.largo = largo
        self.ancho = ancho 
        # Los 7 comportamientos: Normal, Trampa, Resbaladizo, Pegajoso, Viento y Rebote
        self.comportamiento = comportamiento

    def on_collide(self, player):
        self.comportamiento.aplicar(player)

    def on_Bounds(self):
        return self.x, self.y, self.largo, self.ancho
