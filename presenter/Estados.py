from abc import ABC, abstractmethod
import pygame
import sys

from model.GameWorld import GameWorld
from view.View import HEIGHT, WIDTH
from view.Pinicio import PantallaInicio
from view.Castillo import Castillo


class Estado(ABC):
    @abstractmethod
    def manejar_eventos(self):
        pass

    @abstractmethod
    def actualizar(self):
        pass

    @abstractmethod
    def dibujar(self):
        pass


class EstadoInicio(Estado):
    def __init__(self, presenter):
        self.presenter = presenter
        self.pantalla = PantallaInicio(presenter.view.screen, WIDTH, HEIGHT)

    def manejar_eventos(self):
        # PantallaInicio tiene su propio bucle: devuelve "jugar" o "salir"
        resultado = self.pantalla.ejecutar()
        if resultado == "salir":
            self.presenter.salir()
        elif resultado == "jugar":
            return EstadoCastillo(self.presenter)
        return None

    def actualizar(self):
        pass

    def dibujar(self):
        pass


class EstadoCastillo(Estado):
    def __init__(self, presenter):
        self.presenter = presenter
        self.castillo = Castillo(presenter.view.screen, WIDTH, HEIGHT,
                                 presenter.castillo_model)

    def manejar_eventos(self):
        # Castillo tiene su propio bucle: devuelve "torre", "menu" o "salir"
        resultado = self.castillo.ejecutar()
        if resultado == "salir":
            self.presenter.salir()
        elif resultado == "menu":
            return EstadoInicio(self.presenter)
        elif resultado == "torre":
            return EstadoTorre(self.presenter)
        return None

    def actualizar(self):
        pass

    def dibujar(self):
        pass


class EstadoTorre(Estado):
    def __init__(self, presenter):
        self.presenter = presenter
        self.game_world = GameWorld()
        self._cam_y = self.game_world.player.y - HEIGHT // 2

    def manejar_eventos(self):
        if self.presenter.view.check_quit():
            return EstadoPausa(self.presenter, self)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            return EstadoTorre(self.presenter)
        return None

    def actualizar(self):
        gw = self.game_world
        if not gw.won:
            actions = self.presenter.view.get_actions()
            gw.update(actions)

        # Volver al castillo si gana o sale por la derecha
        if gw.ir_castillo:
            # guardar monedas ganadas
            if gw.player.monedas > 0:
                self.presenter.castillo_model.anadir_monedas(gw.player.monedas)
            self.presenter.cambiar_a(EstadoCastillo(self.presenter))
            return

        # camara que sigue al jugador (suave)
        objetivo = gw.player.y - HEIGHT // 2
        self._cam_y += (objetivo - self._cam_y) * 0.1

    def dibujar(self):
        gw = self.game_world
        mensaje = None
        if gw.message:
            mensaje = {'text': gw.message, 'colour': (80, 230, 80)}
        self.presenter.view.draw_frame(gw.player, gw.nivel, self._cam_y, mensaje)


class EstadoPausa(Estado):
    def __init__(self, presenter, estado_anterior):
        self.presenter = presenter
        self.estado_anterior = estado_anterior
        self.font = pygame.font.SysFont(None, 64)
        self.font_sm = pygame.font.SysFont(None, 28)

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.presenter.salir()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return self.estado_anterior   # reanudar
                if event.key == pygame.K_ESCAPE:
                    return EstadoInicio(self.presenter)
        return None

    def actualizar(self):
        pass

    def dibujar(self):
        screen = self.presenter.view.screen
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        txt = self.font.render("PAUSA", True, (255, 255, 255))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 60))

        hint = self.font_sm.render("P para reanudar  -  ESC para menu", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()
        self.presenter.view.clock.tick(60)