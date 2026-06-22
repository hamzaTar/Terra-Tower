import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

# Colours
C_BG = (30, 30, 46)
C_PLATFORM = (80, 80, 105)
C_SLIPPERY = (100, 180, 230)
C_STICKY = (170, 90, 40)
C_BOUNCY = (60, 200, 90)
C_WIND = (80, 230, 160)
C_TRAP = (200, 50, 50)
C_PLAYER = (225, 225, 255)
C_PLAYER_CHG = (255, 210, 50)
C_COIN = (255, 200, 0)
C_COIN_RIM = (200, 150, 0)
C_HUD = (200, 200, 220)
C_WIN_TEXT = (80, 230, 80)
C_DEAD_TEXT = (230, 80, 80)

# not all are used
_BEHAVIOUR_COLOURS = {
    "ComportamientoNormal": C_PLATFORM,
    "ComportamientoResbaladizo": C_SLIPPERY,
    "ComportamientoPegajoso": C_STICKY,
    "ComportamientoRebote": C_BOUNCY,
    "ComportamientoViento": C_WIND,
    "ComportamientoTrampa": C_TRAP,
}


class GameView:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Terra Tower")
        self.clock = pygame.time.Clock()
        self.font_sm = pygame.font.SysFont(None, 22)
        self.font_lg = pygame.font.SysFont(None, 64)

    def get_actions(self) -> list[str]:
        actions = []
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: actions.append("izq")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: actions.append("derch")
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]: actions.append("salta")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: actions.append("down")
        return actions

    def check_quit(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return True
        return False

    # layers 
    def draw_frame(self, player, nivel, cam_y, message=None):
        self.screen.fill(C_BG)
        self._draw_world(nivel, cam_y)
        self._draw_player(player, cam_y)
        self._draw_hud(player, nivel)
        if message: self._draw_message(message)

        pygame.display.flip()
        self.clock.tick(FPS)

    def _draw_world(self, nivel, cam_y):
        for plat in nivel.superficies:
            col = _BEHAVIOUR_COLOURS.get(type(plat.comportamiento).__name__, C_PLATFORM)
            pygame.draw.rect(self.screen, col, (int(plat.x), int(plat.y - cam_y), int(plat.largo), int(plat.ancho)))
        for coin in nivel.moneda:
            if not coin.cogida:
                pygame.draw.circle(self.screen, C_COIN, (int(coin.x + 10), int(coin.y - cam_y + 10)), 10)

    def _draw_player(self, player, cam_y):
        px, py, pw, ph = player.get_Bounds()
        x, y = int(px), int(py - cam_y)

        # 1. Dibujar el jugador base (color normal)
        pygame.draw.rect(self.screen, C_PLAYER, (x, y, int(pw), int(ph)), border_radius=5)

        # 2. Si está cargando, rellenar de amarillo desde abajo
        if player.isCharging:
            fraccion = player.carga / 18  # cuánto está cargado (0 a 1)
            altura_amarilla = int(ph * fraccion)  # altura del relleno
            y_amarillo = y + ph - altura_amarilla  # empieza desde abajo
            pygame.draw.rect(self.screen, C_PLAYER_CHG,
                             (x, y_amarillo, int(pw), altura_amarilla), border_radius=5)

    def _draw_hud(self, player, nivel):
        count = sum(1 for m in nivel.moneda if m.cogida)
        text = f"moneda: {count}/{len(nivel.moneda)} | Puntuación: {player.puntuacion} | Caídas: {player.muertes}"
        surf = self.font_sm.render(text, True, C_HUD)
        self.screen.blit(surf, (10, 10))

    def _draw_message(self, message):
        txt = self.font_lg.render(message['text'], True, message['colour'])
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - txt.get_height() // 2))

    def close(self):
        pygame.quit()