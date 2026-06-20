class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_w = 30
        self.player_h = 30
        self.isOnGround = True
        self.isOnCheckPoint = Flase
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
            self.vy = -2 - 10*self.carga
            self.saltos_restantes -= 1
            self.isOnGround = False
            self.carga = 0
            self.isCharging = False

    def cargar_salto(self):
        self.isCharging = True
        self.carga += 0.1
        if self.carga > 1:
            self.carga = 1

    def gravedad(self):
        self.vy += 0.8
        self.y += self.vy

    def caida_picado(self):
        if not self.isOnGround:
            self.vy = 14

    def aterrizar(self):
        self.isOnGround = True
        self.saltos_restantes = self.saltos_maximos
        self.vy = 0

    def get_Bounds(self):
        return (self.x, self.y, self.player_w, self.player_h)

    def desbloquear_habilidad(self, habilidad):
        self.habilidades[habilidad] = True
        match habilidad:
            case "doubleJump":
                self.saltos_maximos = 2
            case "tripleJump":
                self.saltos_maximos = 3
            case "wallJump":
                self.vx = 2
                self.vy = 5
            case "dash":
                self.vx = 14