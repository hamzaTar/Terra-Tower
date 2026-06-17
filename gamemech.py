import pygame
import sys

# --- SETTINGS ---
WIDTH = 800
HEIGHT = 500
FPS = 60

GRAVITY = 0.6
JUMP_FORCE_MIN = -10
JUMP_FORCE_MAX = -18
JUMP_CHARGE_FRAMES = 30   # frames to hold space for max jump
MOVE_SPEED = 5

PLAYER_W = 30
PLAYER_H = 30

WALL_W = 30   # thickness of side walls

# Tower platforms — y=0 is the TOP of the world, increases downward
# World is tall; camera follows player upward
# Each platform: (x, y, width, height)
# x is relative to the play area (not counting wall)
# Play area width = WIDTH - 2*WALL_W = 740
PLAY_W = WIDTH - 2 * WALL_W  # 740

PLATFORMS = [
    # Ground floor
    (0,   1800, PLAY_W, 20),

    # Layer 1
    (50,  1680, 160, 15),
    (350, 1650, 160, 15),
    (560, 1700, 160, 15),

    # Layer 2
    (100, 1530, 140, 15),
    (320, 1490, 140, 15),
    (520, 1540, 140, 15),

    # Layer 3
    (200, 1380, 160, 15),
    (430, 1350, 140, 15),
    (60,  1320, 130, 15),

    # Layer 4
    (300, 1220, 150, 15),
    (520, 1180, 140, 15),
    (100, 1170, 130, 15),

    # Layer 5
    (200, 1050, 140, 15),
    (440, 1020, 140, 15),
    (620, 1060, 100, 15),

    # Layer 6
    (50,  920,  130, 15),
    (280, 890,  150, 15),
    (510, 870,  130, 15),

    # Layer 7
    (150, 760,  140, 15),
    (390, 730,  140, 15),
    (600, 750,  120, 15),

    # Layer 8
    (80,  620,  130, 15),
    (310, 590,  150, 15),
    (540, 610,  130, 15),

    # Layer 9
    (180, 470,  140, 15),
    (420, 450,  140, 15),
    (610, 480,  110, 15),

    # Layer 10 — near top
    (60,  340,  130, 15),
    (280, 310,  150, 15),
    (500, 290,  140, 15),

    # Very top
    (250, 180,  240, 20),
]

WORLD_HEIGHT = 1900  # total height of the tower world

###############################

class Player:
    def __init__(self):
        self.x = float(PLAY_W // 2 - PLAYER_W // 2)
        self.y = float(1750)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.jump_held = 0      # frames space is held while on ground
        self.jump_charging = False

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), PLAYER_W, PLAYER_H)

    def handle_input(self, keys):
        # Horizontal
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = MOVE_SPEED

        # Jump charging: hold space while on ground to charge
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.on_ground:
                self.jump_charging = True
                self.jump_held = min(self.jump_held + 1, JUMP_CHARGE_FRAMES)
        else:
            # Key released — fire jump if was charging
            if self.jump_charging and self.on_ground:
                t = self.jump_held / JUMP_CHARGE_FRAMES
                self.vy = JUMP_FORCE_MIN + (JUMP_FORCE_MAX - JUMP_FORCE_MIN) * t
                self.on_ground = False
            self.jump_charging = False
            self.jump_held = 0

    def update(self, platforms):
        # Gravity
        self.vy += GRAVITY
        if self.vy > 20:
            self.vy = 20   # terminal velocity

        # --- Horizontal movement + wall collision ---
        self.x += self.vx
        # Left wall (play area starts at 0)
        if self.x < 0:
            self.x = 0
        # Right wall
        if self.x + PLAYER_W > PLAY_W:
            self.x = PLAY_W - PLAYER_W

        # --- Vertical movement with swept collision ---
        steps = max(1, int(abs(self.vy) / 8) + 1)
        dy = self.vy / steps
        self.on_ground = False

        for _ in range(steps):
            self.y += dy
            rect = self.get_rect()

            for plat in platforms:
                if rect.colliderect(plat):
                    if dy > 0:
                        # Moving down — land on top
                        self.y = plat.top - PLAYER_H
                        self.vy = 0
                        dy = 0
                        self.on_ground = True
                    elif dy < 0:
                        # Moving up — hit ceiling
                        self.y = plat.bottom
                        self.vy = 0
                        dy = 0
                    rect = self.get_rect()

        # Floor of world
        if self.y + PLAYER_H > WORLD_HEIGHT:
            self.y = WORLD_HEIGHT - PLAYER_H
            self.vy = 0
            self.on_ground = True

    def draw(self, surface, cam_y):
        draw_y = int(self.y) - cam_y
        pygame.draw.rect(surface, (0, 0, 0),
                         (WALL_W + int(self.x), draw_y, PLAYER_W, PLAYER_H))

        # Draw charge bar above player when charging
        if self.jump_charging and self.jump_held > 0:
            bar_w = int((self.jump_held / JUMP_CHARGE_FRAMES) * PLAYER_W)
            pygame.draw.rect(surface, (200, 0, 0),
                             (WALL_W + int(self.x), draw_y - 8, bar_w, 5))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tower Platformer")
    clock = pygame.time.Clock()

    plat_rects = [pygame.Rect(x, y, w, h) for (x, y, w, h) in PLATFORMS]

    player = Player()
    font = pygame.font.SysFont("courier", 13)

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
        player.update(plat_rects)

        # Camera: smoothly follow player, anchor at bottom when near floor
        target_cam_y = int(player.y) - HEIGHT // 2
        target_cam_y = max(0, min(target_cam_y, WORLD_HEIGHT - HEIGHT))

        try:
            cam_y += int((target_cam_y - cam_y) * 0.15)
        except NameError:
            cam_y = target_cam_y

        # --- Draw ---
        screen.fill((240, 240, 240))

        # Platforms
        for plat in plat_rects:
            draw_y = plat.y - cam_y
            if -20 < draw_y < HEIGHT + 20:
                pygame.draw.rect(screen, (0, 0, 0),
                                 (WALL_W + plat.x, draw_y, plat.width, plat.height))

        # Player
        player.draw(screen, cam_y)

        # Side walls
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WALL_W, HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), (WIDTH - WALL_W, 0, WALL_W, HEIGHT))

        # HUD
        hint = font.render("Hold SPACE longer = higher jump  |  A/D or arrows to move", True, (120, 120, 120))
        screen.blit(hint, (WALL_W + 10, 10))

        height_val = max(0, WORLD_HEIGHT - int(player.y))
        h_text = font.render(f"Height: {height_val}", True, (80, 80, 80))
        screen.blit(h_text, (WALL_W + 10, 28))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
