class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isOnGround = True
        self.isCharging = False
        self.vx = 4
        self.vy = 6
        # Puntuación y monedas
        self.puntuacion = 0
        self.monedas = 0
        # Para habilidades
        self.saltos_restantes = 1
        self.habilidades = []

    def movimiento(self, direccion):
        if direccion == "izq":
            self.x -= self.vx
        elif direccion == "derch":
            self.x += self.vx

    def saltar(self):
        for i in self.habilidades:
            if i == "doubleJump":
                self.saltos_restantes += 1
        if self.isOnGround:
            self.y -= self.vy
            self.saltos_restantes -= 1
            if not self.isOnGround and self.saltos_restantes > 0:

    def gravedad(self):
        pass

    def caida_picado(self):
        if not self.isOnGround:
            self.y += self.vy