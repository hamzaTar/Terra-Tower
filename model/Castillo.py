import pygame
from model.Player import Player

# --- Colores ---
c_cielo = (100, 160, 220)
c_suelo = (60, 130, 40)
c_suelo_sombra = (45, 95, 30)

c_interior = (240, 235, 220)
c_muro_ext = (80, 80, 85)
c_tejado = (140, 60, 45)
c_puerta_fill = (200, 185, 160)
c_puerta_marc = c_muro_ext
c_pomo = c_muro_ext
c_jugador = (100, 150, 220)

# --- Parametros ---
posx_cast = 0
posy_cast = 190
ancho_cast = 800
alto_cast = 370
posy_suelo = posy_cast + alto_cast
espesor = 5

posx_punta, posy_punta = ancho_cast // 2, 30

num_col = 2
num_filas = 2
ancho_habitacion = ancho_cast // num_col
alto_habitacion = alto_cast // num_filas

ancho_puerta = 65
alto_puerta = 105
espesor_puerta = 12

class Castillo:
    def __init__(self, aparienza, ancho, alto, modelo, pos_inicio = None):
        self.aparienza = aparienza
        self.ancho = ancho
        self.alto = alto
        self.modelo = modelo
        self.font_sm = pygame.font.SysFont(None, 22)
        self.relog = pygame.time.Clock()
        self.sombra = pygame.Surface((ancho_habitacion, alto_habitacion), pygame.SRCALPHA)
        self.sombra.fill((0, 0, 0, 160))
        posx_ini_jugador = pos_inicio if pos_inicio is not None else ancho_habitacion // 2
        self.jugador = Player(posx_ini_jugador, posy_suelo - 30, False)

    def ejecutar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return 'salir'
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return 'menu'

            self.actualizar_jugador()

            if self.jugador.x + self.jugador.player_w < 0:
                return 'torre'

            self.dibujar()
            pygame.display.flip()
            self.relog.tick(60)

    def actualizar_jugador(self):
        p = self.jugador
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            p.movimiento("izq")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            p.movimiento("derch")
        else:
            p.movimiento("")
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and p.isOnGround:
            p.carga = 12
            p.saltar()

        p.gravedad()
        p.x += p.vx
        p.y += p.vy

        # Suelo del castillo
        if p.y + p.player_h >= posy_suelo:
            p.y = posy_suelo - p.player_h
            p.aterrizar()

        # Techo: no salir por arriba
        if p.y < posy_cast:
            p.y = float(posy_cast)
            p.vy = 0

        # Límite derecho: no puede salir
        if p.x + p.player_w > ancho_cast:
            p.x = float(ancho_cast - p.player_w)
            p.vx = 0

        self.bloquear_paso()

    def bloquear_paso(self):
        p = self.jugador
        p_rect = pygame.Rect(int(p.x), int(p.y), p.player_w, p.player_h)

        for i, desbloqueada in enumerate(self.modelo.habitaciones):
            if not desbloqueada:
                rect_hab = self.rect_habitacion(i)
                if p_rect.colliderect(rect_hab):
                    if p.vx > 0:
                        p.x = float(rect_hab.left - p.player_w)
                    elif p.vx < 0:
                        p.x = float(rect_hab.right)
                    p.vx = 0

    def rect_habitacion(self, indice):
        fila = 1 if indice < 3 else 0
        col = indice if indice < 3 else indice - 3
        posx = posx_cast + col * ancho_habitacion
        posy = posy_cast + fila * alto_habitacion
        return pygame.Rect(posx, posy, ancho_habitacion, alto_habitacion)

    def dibujar(self):
        self.dibujar_fondo()
        self.dibujar_relleno_interior()
        self.dibujar_puerta_izquierda()
        self.dibujar_muros_exteriores()
        self.dibujar_sombreado_bloqueadas()
        self.dibujar_jugador()
        self.dibujar_marcador()

    def dibujar_fondo(self):
        self.aparienza.fill(c_cielo, pygame.Rect(0, 0, self.ancho, posy_suelo))
        self.aparienza.fill(c_suelo, pygame.Rect(0, posy_suelo, self.ancho, self.alto - posy_suelo))
        self.aparienza.fill(c_suelo_sombra, pygame.Rect(0, posy_suelo, self.ancho, 10))

    def dibujar_relleno_interior(self):
        pygame.draw.rect(self.aparienza, c_interior, pygame.Rect(posx_cast, posy_cast, ancho_cast, alto_cast))
        pygame.draw.polygon(self.aparienza, c_tejado, [(posx_cast, posy_cast), (posx_cast + ancho_cast, posy_cast),
                                                       (posx_punta, posy_punta)])

    def dibujar_puerta_izquierda(self):
        px = 0
        py = posy_suelo - alto_puerta
        pygame.draw.rect(self.aparienza, c_puerta_fill, pygame.Rect(px, py, ancho_puerta, alto_puerta))
        pygame.draw.rect(self.aparienza, c_puerta_marc, pygame.Rect(px, py, ancho_puerta, alto_puerta), 2)
        pygame.draw.circle(self.aparienza, c_pomo, (px + ancho_puerta - 12, py + alto_puerta // 2), 5)


    def dibujar_muros_exteriores(self):
        pygame.draw.rect(self.aparienza, c_muro_ext, pygame.Rect(posx_cast, posy_cast, ancho_cast, alto_cast), espesor)

    def dibujar_sombreado_bloqueadas(self):
        for i, desbloqueada in enumerate(self.modelo.habitaciones):
            if not desbloqueada:
                rect = self.rect_habitacion(i)
                self.aparienza.blit(self.sombra, rect.topleft)

    def dibujar_jugador(self):
        p = self.jugador
        pygame.draw.rect(self.aparienza, c_jugador,
                         pygame.Rect(int(p.x), int(p.y), p.player_w, p.player_h),
                         border_radius=4)

    def dibujar_marcador(self):
        texto = self.font_sm.render(
            f"moneda: {self.modelo.monedas} | Puntuación: {self.jugador.puntuacion}",
            True, (200, 200, 220))
        self.aparienza.blit(texto, (10, 10))