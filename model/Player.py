class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isOnGround = True
        self.isOnCheckPoint = False
        self.isCharging = False
        self.vx = 4
        self.vy = 6
        # Puntuación y monedas
        self.puntuacion = 0
        self.monedas = 0
        # Para habilidades
        self.saltos_restantes = 1
        self.habilidades = {"doubleJump": False, "wallJump": False, "dash": False}

    def movimiento(self, direccion):
        if direccion == "izq":
            self.x -= self.vx
        elif direccion == "derch":
            self.x += self.vx

    def saltar(self):
        if self.habilidades.values("doubleJump") == True and self.saltos_restantes > 0:
            self.y -= self.vy
            self.saltos_restantes -= 1
            self.isOnGround = False
            Player.saltar()
        elif self.habilidades.values("doubleJump") == True and self.saltos_restantes == 1:
            self.y -= self.vy
            self.saltos_restantes -= 1
            self.isOnGround = False

    def gravedad(self):
        pass

    def caida_picado(self):
        if not self.isOnGround:
            self.y += self.vy