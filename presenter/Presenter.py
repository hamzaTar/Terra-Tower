import pygame
import sys

from model.GameWorld import GameWorld
from view.View import GameView, HEIGHT, WIDTH
from model.Pinicio import PantallaInicio
from model.Castillo import Castillo
from model.CastilloModel import CastilloModel


class GamePresenter:
    def __init__(self):
        self.view = GameView()
        self.castillo_model = CastilloModel()
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

            # Bucle torre <-> castillo
        while True:
            castillo = Castillo(self.view.screen, WIDTH, HEIGHT, self.castillo_model)
            resultado_castillo = castillo.ejecutar()

            if resultado_castillo == 'salir':
                self.view.close()
                sys.exit()

            if resultado_castillo == 'menu':
                # Volver a la pantalla de inicio
                pantalla_inicio = PantallaInicio(self.view.screen, WIDTH, HEIGHT)
                res = pantalla_inicio.ejecutar()
                if res == 'salir':
                    self.view.close()
                    sys.exit()
                continue

            self._init_game()
            resultado_torre = self._bucle_torre()

            if resultado_torre == 'salir':
                self.view.close()
                sys.exit()

            monedas_ganadas = self.game_world.player.monedas
            if monedas_ganadas > 0:
                self.castillo_model.anadir_monedas(monedas_ganadas)

    def _bucle_torre(self):
        while True:
            if self.view.check_quit():
                return 'salir'

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self._init_game()
                continue

            if not self.game_world.won:
                actions = self.view.get_actions()
                self.game_world.update(actions)

            if self.game_world.ir_castillo:
                return 'castillo'

            py = self.game_world.player.y
            self._cam_y = (int(py) // HEIGHT) * HEIGHT

            mensaje = None
            if self.game_world.message:
                mensaje = {'text': self.game_world.message, 'colour': (80, 230, 80)}

            self.view.draw_frame(self.game_world.player, self.game_world.nivel, self._cam_y, mensaje)