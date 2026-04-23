import pygame
import sys

# --- SETTINGS ---
WIDTH = 800
HEIGHT = 500
FPS = 60

GRAVITY = 0.5
JUMP_FORCE = -12
MOVE_SPEED = 5

PLAYER_W = 30
PLAYER_H = 30

# Platform layout: (x, y, width, height)
PLATFORMS = [
    (0,   460, 200, 20),
    (250, 460, 300, 20),
    (600, 460, 200, 20),
    (100, 360, 150, 15),
    (350, 290, 150, 15),
    (580, 220, 150, 15),
    (200, 200, 120, 15),
    (480, 140, 130, 15),
    (50,  130, 120, 15),
    (670, 100, 130, 15),
]


class Player:
    def __init__(self):
        self.x = 50.0
        self.y = 400.0
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.rect = pygame.Rect(self.x, self.y, PLAYER_W, PLAYER_H)

    def handle_input(self, keys):
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = MOVE_SPEED
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

    def update(self, platforms):
        # Gravity
        self.vy += GRAVITY

        # Move X + screen wrap
        self.x += self.vx
        if self.x + PLAYER_W < 0:
            self.x = WIDTH
        if self.x > WIDTH:
            self.x = -PLAYER_W

        # Move Y
        self.y += self.vy
        self.on_ground = False

        # Update rect for collision
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Platform collision
        for plat in platforms:
            if self.rect.colliderect(plat):
                # Falling down -> land on top
                if self.vy >= 0 and self.rect.bottom - self.vy <= plat.top:
                    self.y = plat.top - PLAYER_H
                    self.vy = 0
                    self.on_ground = True
                # Jumping up -> hit bottom
                elif self.vy < 0 and self.rect.top - self.vy >= plat.bottom:
                    self.y = plat.bottom
                    self.vy = 0
                self.rect.y = int(self.y)

        # Fall off bottom -> respawn
        if self.y > HEIGHT + 50:
            self.x = 50
            self.y = 400
            self.vy = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (int(self.x), int(self.y), PLAYER_W, PLAYER_H))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    platforms = [pygame.Rect(x, y, w, h) for (x, y, w, h) in PLATFORMS]

    player = Player()

    font = pygame.font.SysFont("courier", 14)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update(platforms)

        screen.fill((255, 255, 255))

        for plat in platforms:
            pygame.draw.rect(screen, (0, 0, 0), plat)

        player.draw(screen)

        hint = font.render("Arrow keys / WASD  |  Up / W / Space to jump  |  ESC to quit", True, (150, 150, 150))
        screen.blit(hint, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
