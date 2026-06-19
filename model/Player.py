class Player:
    def __init__(self, x, y, isOnCheckPoint):
        self.x = x
        self.y = y
        self.isOnGround = True
        self.isOnCheckPoint = isOnCheckPoint
        self.vx = 4
        self.vy = 6
        self.saltos_restantes = 1
        self.saltos_maximos = 1
        self.isCharging = False
        self.carga = 0 # Tanto por uno nos indica del porcentaje de carga del salto
        # Puntuación y monedas
        self.puntuacion = 0
        self.monedas = 0
        # Para habilidades
        self.habilidades = {"doubleJump": False, "tripleJump": False, "wallJump": False, "dash": False}

    def movimiento(self, direccion):
        if direccion == "izq":
            self.x -= self.vx
        elif direccion == "derch":
            self.x += self.vx

    def saltar(self):
        if self.saltos_restantes > 0:
            self.vy = -12
            self.saltos_restantes -= 1
            self.isOnGround = False

    def gravedad(self):
        self.vy += 0.8
        self.y += self.vy

    def caida_picado(self):
        if not self.isOnGround:
            self.vy = 14

    def aterrizar(self):
        self.isOnGround = True
        self.saltos_restantes = 1
        self.vy = 0


    def get_Bounds(self):
        ancho = 800
        alto = 500
        ancho_paredes = 30

    def desbloquear_habilidad(self, habilidad):
        self.habilidades[habilidad] = True
        if self.habilidades["doubleJump"] == True:
            self.saltos_maximos = 2
        elif self.habilidades["tripleJump"] == True:
            self.saltos_maximos = 3
        elif self.habilidades["wallJump"] == True:
            pass
        elif self.habilidades["dash"] == True:
            self.vx = 14