class Player:
    def __init__(self, x, y, isOnCheckPoint):
        self.x = x
        self.y = y
        self.player_w = 30
        self.player_h = 30
        self.isOnGround = True
        self.isOnCheckPoint = isOnCheckPoint
        self.vx = 0.0
        self.vy = 0.0
        self.saltos_restantes = 1
        self.saltos_maximos = 1
        self.isCharging = False
        self.carga = 0.0               
        self.jump_dir = 0              
        self.facing = 1                
        self.puntuacion = 0
        self.monedas = 0
        self.habilidades = {
            "doubleJump": False,
            "tripleJump": False,
            "wallJump": False,
            "dash": False
        }


    # Hecho en presenter
    def movimiento(self, direccion):
        pass   

    def cargar_salto(self):
        self.isCharging = True
        self.carga += 0.6  
        if self.carga > 18.0:
            self.carga = 18.0

    def saltar(self):
        if self.saltos_restantes > 0:
            self.vy = -self.carga
            self.vx = self.jump_dir * (self.carga * 0.45)
            self.saltos_restantes -= 1
            self.isOnGround = False
            self.carga = 0.0
            self.isCharging = False

    def gravedad(self):
        self.vy += 0.6 

    def caida_picado(self):
        if not self.isOnGround:
            self.vy = 14

    def aterrizar(self):
        self.isOnGround = True
        self.saltos_restantes = self.saltos_maximos
        self.vy = 0.0

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
