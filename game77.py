
import pygame
import sys

# --- CONFIG ---
WIDTH, HEIGHT = 800, 640
FPS = 60
TILE_SIZE = 40 # 20 columns (800) x 15 rows (600) per screen

GRAVITY = 0.6
WALK_SPEED = 5
MAX_JUMP_FORCE = 18
CHARGE_RATE = 0.6
WALL_BOUNCE = 0.7

# --- THE MATRIX (Draw your level here!) ---
# Screen 1 is the top, Screen 0 is the bottom. 
# 15 lines of text = 1 screen.
LEVEL_MAP = [
    # --- SCREEN 10 (Top: Boss Arena Placeholder) ---
    "XXXXXXXXXXXXXXXXXXXX",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X        B         X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",

    # --- SCREEN 9 (Really, really hard jump) ---
    "X                  X",
    "X                  X",
    "XXXXXXXXXXXXXXXX   X", # Giant wall blocking you, forcing a precise right-jump
    "X                  X",
    "X                  X",
    "X              X   X",
    "X           P      X",
    "X           X      X",
    "X                  X",
    "X  F               X", # A cruel fake block right before the top!
    "XXXX               X",
    "X                  X",
    "X                  X",
    "X           X      X", # Tiny 1-block landing zone
    "X                  X",
    "X      XX          X",
    "X      XX          X",
    "X                  X",
    "X        XX        X",

    "X                  X",
    "X               XX X",
    "X                  X",
    "X B                X", # Shooter monster on left
    "XXXX               X",
    "X  E               X", # Hidden chest beneath the shooter!
    "XXXXX         XX   X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X    XX            X",
    "X                  X",
    # --- SCREEN 7 (First Patrol Monster) ---
    "X                  X",
    "X                  X",
    "XXXXXXXXX          X",
    "XXXXXXXXX          X", # Thick floor separating the zones

    "XXXXXXXXX          X",
    "X                 XX",
    "X  M               X", # Monster pacing back and forth
    "X XXXX             X",
    "X                  X",
    "X                  X",
    "X         M        X", # Monster guarding a wide platform
    "X       XXXXXX     X",
    "X                  X",
    "X                  X",
    "X    XXXX          X",
    "X                  X",
    # --- SCREEN 6 (Normal / Breather + Climbing Intro) ---
    "X                  X",
    "X           XXXXX  X",
    "X                  X",

    "X                  X",
    "X                  X",
    "X     XXXXX        X",
    "X     C            X", # Vines/Ladder hanging down
    "X     C            X",
    "X     C            X",
    "X   XXX            X",
    "X                  X",
    "X             XXXX X",
    "X                  X",
    "X                  X",
    "X   XXXX           X",
    "X                  X",
    # --- SCREEN 5 (Wind + Fake Blocks) ---
    "X                  X",
    "X                  X",

    "X                  X",
    "X                  X",
    "X              XXX X",
    "X                  X",
    "X         FF       X", # Looks like a safe jump, but it breaks!
    "X                  X",
    "X                  X",
    "X                  X",
    "X     XXXX         X",
    "X                  X",
    "X   WWWWWWWWWWWWWWW ",
    "X                  X",
    "X                  X",
    "X             XXXX X",
    # --- SCREEN 4 (Wind Intro) ---
    "X                  X",
    "X                  X",
    "X       XXX     XXXX",

    "XX                 X",
    "X                  X",
    "X                  X", # Heavy wind pushing left
    "X          XXXXXXXXX",
    "X                  X",
    "X                  X",
    "XXX                X",
    "X   WWWWWWWWWWWWWWW ",
    "X               WWW ",
    "X             WWWWW ",
    "X           WWWWWWW ",
    "X   WWWWWWWWWWWWWWW ",
    "X         XXXXXXXXXX",
    # --- SCREEN 3 (First Difficulty Spike) ---
    "X                  X",
    "X                  X",
    "X                  X",

    "X                  X",
    "X  XXXX            X",
    "X                  X",
    "X         XX       X", # Very small landing pads
    "X                  X",
    "X                  X",
    "X               XX X",
    "X                  X",
    "X                  X",
    "X       XX         X",
    "X                  X",
    "X                  X",
    "X   XX             X",
    # --- SCREEN 3 (Still Easy + Hidden Secret) ---
    "X                  X",
    "X                  X",
    "X                  X",


    "X   XXX            X",
    "X   XXXX           X",
    "X              XXXXX",
    "X                  X",
    "X          XXX     X",
    "X                  X",
    "X                  X",
    "X    XXX           X",
    "X                  X",
    "XX           X     X", # Looks like a wall...
    "XE         XXX     X", # ...but you can jump inside for a chest!
    "XXX                X",
    "X                  X",
    # --- SCREEN 2 (Bottom: Easy Tutorial) ---
    "X                  X",
    "X   XXXX           X",
    "X                  X",
    "X           XXXXXXXX",
    "X                  X",
    "XXXX               X",
    "X                  X",
    "X                  X",
    "X            XXXXXXX",
    "X                  X",
    "X  XXX             X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                  X",
    "XXXXXXXX           X",
    # --- SCREEN 1 (Bottom: Easy Tutorial) ---
    "X                  X",
    "X              XXXXX",
    "X                  X",
    "X                  X",
    "X                  X",
    "X        XXX       X",
    "X                  X",
    "X                  X",
    "XXXX               X",
    "X                  X",
    "X                  X",
    "X                  X",
    "X                   ",
    "X                   ",
    "XXXXXXXXXXXXXXXXXXXX",
]
class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 25, 25) # Position set by map parser
        self.vx = 0
        self.vy = 0
        self.charge = 0
        self.is_charging = False
        self.on_ground = False
        self.jump_direction = 0
        self.start_x = 0
        self.start_y = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.on_ground:
            if keys[pygame.K_SPACE]:
                self.is_charging = True
                self.vx = 0
                self.charge = min(self.charge + CHARGE_RATE, MAX_JUMP_FORCE)
                if keys[pygame.K_LEFT]: self.jump_direction = -1
                elif keys[pygame.K_RIGHT]: self.jump_direction = 1
                else: self.jump_direction = 0
            elif self.is_charging:
                self.vy = -self.charge
                self.vx = self.jump_direction * (self.charge * 0.45)
                self.is_charging = False
                self.charge = 0
                self.on_ground = False
            else:
                if keys[pygame.K_LEFT]: self.vx = -WALK_SPEED
                elif keys[pygame.K_RIGHT]: self.vx = WALK_SPEED
                else: self.vx = 0

    def apply_physics(self, platforms, hazards, winds):
        for w in winds:
            if self.rect.colliderect(w['rect']):
                self.vx += w['force']

        self.vy += GRAVITY
        
        # X Move & Bounce
        self.rect.x += self.vx
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vx > 0:
                    self.rect.right = p.left
                    self.vx = -self.vx * WALL_BOUNCE
                elif self.vx < 0:
                    self.rect.left = p.right
                    self.vx = -self.vx * WALL_BOUNCE

        # Y Move
        self.on_ground = False
        self.rect.y += self.vy
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.vx = 0 
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.bottom
                    self.vy = 0

        # Spikes / Death
        for h in hazards:
            if self.rect.colliderect(h):
                self.rect.x = self.start_x
                self.rect.y = self.start_y

def load_level(level_map, player):
    platforms = []
    hazards = []
    winds = []
    
    # Calculate how many total rows we have so we can set the starting Y correctly.
    # In Jump King, you start at the bottom and go UP into negative Y space.
    total_rows = len(level_map)
    lowest_y = (total_rows - 15) * TILE_SIZE # The Y coordinate of the top of the bottom screen
    
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            # Calculate actual X and Y in the world
            x = col_index * TILE_SIZE
            # We offset the Y so the bottom screen starts at Y=0
            y = (row_index * TILE_SIZE) - lowest_y
            
            if tile == 'X':
                platforms.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif tile == 'S':
                # Make spikes a little shorter than a full block
                hazards.append(pygame.Rect(x, y + 20, TILE_SIZE, 20))
            elif tile == 'W':
                # Wind zone pushes left
                winds.append({'rect': pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), 'force': -0.4})
            elif tile == 'P':
                player.rect.x = x
                player.rect.y = y
                player.start_x = x
                player.start_y = y

    return platforms, hazards, winds

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    player = Player()
    
    # Let the computer build the level for you!
    platforms, hazards, winds = load_level(LEVEL_MAP, player)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        player.handle_input()
        player.apply_physics(platforms, hazards, winds)

        # --- THE JUMP KING CAMERA TRICK ---
        # Integer division (//) finds out which 600px chunk the player is in.
        # If player Y is 400: (400 // 600) * 600 = 0. Camera is at 0.
        # If player Y is -100: (-100 // 600) * 600 = -600. Camera snaps to -600!
        camera_y = (player.rect.centery // HEIGHT) * HEIGHT

        screen.fill((30, 30, 30))
        
        # Draw Wind
        for w in winds:
            wind_surface = pygame.Surface((w['rect'].width, w['rect'].height), pygame.SRCALPHA)
            wind_surface.fill((100, 255, 100, 30))
            screen.blit(wind_surface, (w['rect'].x, w['rect'].y - camera_y))

        # Draw World
        for p in platforms: pygame.draw.rect(screen, (100, 100, 100), (p.x, p.y - camera_y, p.width, p.height))
        for h in hazards: pygame.draw.rect(screen, (0, 0, 0), (h.x, h.y - camera_y, h.width, h.height))
        
        # Draw Player
        color = (255, 255, 255) if not player.is_charging else (255, 200, 0)
        pygame.draw.rect(screen, color, (player.rect.x, player.rect.y - camera_y, player.rect.width, player.rect.height))
        
        if player.is_charging:
            bar_w = (player.charge / MAX_JUMP_FORCE) * 30
            pygame.draw.rect(screen, (255, 0, 0), (player.rect.x, player.rect.y - camera_y - 10, bar_w, 5))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
