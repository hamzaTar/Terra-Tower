import pygame
import sys

from model.GameWorld import GameWorld
from view.View import GameView, HEIGHT, WIDTH
from model.Pinicio import PantallaInicio


class GamePresenter:
    def __init__(self):
        self.view = GameView()
        self._init_game()

    def _init_game(self):
        # El Modelo se encarga de TODA la logica.
        self.game_world = GameWorld()
        self._cam_y = self.game_world.player.y - HEIGHT // 2

    def run(self):

        # 0. Display pantalla de inicio
        pantalla_inicio = PantallaInicio(self.view.screen, WIDTH, HEIGHT)
        display = pantalla_inicio.ejecutar()
        if display == 'salir':
            self.view.screen.close()
            sys.exit()

        while True:
            # 1. Comprobar si se quiere salir
            if self.view.check_quit():
                self.view.close()
                sys.exit()

            # 2. Reinicio con tecla R
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self._init_game()
                continue

            # 3. Pedir acciones a la Vista y pasarlas al Modelo
            if not self.game_world.won:
                actions = self.view.get_actions()
                self.game_world.update(actions)

            # 4. Calcular camara (esto es responsabilidad de presentacion)
            py = self.game_world.player.y
            self._cam_y = (int(py) // HEIGHT) * HEIGHT

            # 5. Decirle a la Vista que pinte el estado actual
            mensaje = None
            if self.game_world.message:
                mensaje = {'text': self.game_world.message, 'colour': (80, 230, 80)}

            self.view.draw_frame(
                self.game_world.player,
                self.game_world.nivel,
                self._cam_y,
                mensaje
            )