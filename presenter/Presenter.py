import pygame
import sys

from model.Player import Player
from model.Nivel  import Nivel
from view.View import GameView, HEIGHT, WIDTH, C_WIN_TEXT
from model.Nivel import TILE_SIZE
from model.Pinicio import PantallaInicio

COIN_SIZE   = 30
COIN_POINTS = 10
GRAVITY_MAX = 20
MOVE_SPEED  = 5       
WIND_FORCE  = -0.3    
WALL_BOUNCE = 0.7

class GamePresenter:
    def __init__(self):
        self.view = GameView()
        self._init_game()

    def _init_game(self):
        self.nivel = Nivel()
        self.nivel.cargar()
        self.player = Player(
            x=self.nivel.spawn_x,
            y=self.nivel.spawn_y,
            isOnCheckPoint=False,
        )
        self._hspeed  = 0
        self._cam_y   = self.nivel.spawn_y - HEIGHT // 2
        self._message = None
        self._won     = False

    def run(self):
        pantalla_inicio = PantallaInicio(self.view.screen, WIDTH, HEIGHT)
        resultado = pantalla_inicio.ejecutar()

        if resultado == "salir":
            self.view.close()
            sys.exit()

        while True:
            if self.view.check_quit():
                self.view.close()
                sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self._init_game()
                continue

            if not self._won:
                actions = self.view.get_actions()
                self._update(actions)

            _, py, _, _ = self.player.get_Bounds()
            
            self._cam_y = (int(py) // HEIGHT) * HEIGHT

            self.view.draw_frame(self.player, self.nivel, self._cam_y, self._message)

    def _update(self, actions):
        p = self.player

        if p.isCharging:
            p.vx = 0.0  
            if "izq" in actions:
                p.jump_dir = -1
                p.facing = -1
            elif "derch" in actions:
                p.jump_dir = 1
                p.facing = 1
            else:
                p.jump_dir = 0
        else:
            if p.isOnGround:
                if "izq" in actions:
                    p.vx = -MOVE_SPEED
                    p.facing = -1
                    p.jump_dir = -1
                elif "derch" in actions:
                    p.vx = MOVE_SPEED
                    p.facing = 1
                    p.jump_dir = 1
                else:
                    p.vx = 0
                    p.jump_dir = 0

        if "jump" in actions:
            if p.isOnGround:
                p.cargar_salto()
        else:
            if p.isCharging:
                p.saltar()

        if "down" in actions:
            p.caida_picado()

        p.gravedad()
        if p.vy > GRAVITY_MAX:
            p.vy = GRAVITY_MAX
            
        self._apply_wind()

        p.x += p.vx
        self._collide_x()

        p.y += p.vy
        self._collide_y()

        self._check_coins()

        # when you win 
        goal_rect = pygame.Rect(self.nivel.goal_x, self.nivel.goal_y, TILE_SIZE, TILE_SIZE)
        player_rect = pygame.Rect(int(p.x), int(p.y), p.player_w, p.player_h)

        if player_rect.colliderect(goal_rect):
            self._won = True
            self._message = {'text': '¡Has ganado!', 'colour': C_WIN_TEXT}

    def _apply_wind(self):
        p  = self.player
        px, py, pw, ph = p.get_Bounds()
        pr = pygame.Rect(px, py, pw, ph)
        for surf in self.nivel.superficies:
            if type(surf.comportamiento).__name__ == 'ComportamientoViento':
                sr = pygame.Rect(surf.x, surf.y, surf.largo, surf.ancho)
                if pr.colliderect(sr):
                    p.vx += WIND_FORCE  

    def _collide_x(self):
        p = self.player
        pw, ph = p.player_w, p.player_h
        pr = pygame.Rect(int(p.x), int(p.y), pw, ph)

        for surf in self.nivel.superficies:
            if type(surf.comportamiento).__name__ == 'ComportamientoViento':
                continue
            sr = pygame.Rect(surf.x, surf.y, surf.largo, surf.ancho)
            
            if pr.colliderect(sr):
                if p.vx > 0:            
                    p.x = surf.x - pw
                    p.vx = -p.vx * WALL_BOUNCE
                elif p.vx < 0:          
                    p.x = surf.x + surf.largo
                    p.vx = -p.vx * WALL_BOUNCE
                
                pr.x = int(p.x)

    def _collide_y(self):
        p = self.player
        pw, ph = p.player_w, p.player_h
        p.isOnGround = False
        pr = pygame.Rect(int(p.x), int(p.y), pw, ph)

        for surf in self.nivel.superficies:
            if type(surf.comportamiento).__name__ == 'ComportamientoViento':
                continue
            sr = pygame.Rect(surf.x, surf.y, surf.largo, surf.ancho)
            
            if pr.colliderect(sr):
                if p.vy >= 0:           
                    p.y = surf.y - ph
                    p.aterrizar()
                    surf.on_collide(p)
                elif p.vy < 0:          
                    p.y = surf.y + surf.ancho
                    p.vy = 0.0
                
                pr.y = int(p.y)

    def _check_coins(self):
        p  = self.player
        pr = pygame.Rect(int(p.x), int(p.y), p.player_w, p.player_h)
        for coin in self.nivel.moneda:
            if coin.cogida:
                continue
            cr = pygame.Rect(coin.x, coin.y, COIN_SIZE, COIN_SIZE)
            if pr.colliderect(cr):
                coin.cogida   = True
                p.moneda    += 1
                p.puntuacion += COIN_POINTS
