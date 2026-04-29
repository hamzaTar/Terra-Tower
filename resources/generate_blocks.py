from PIL import Image, ImageDraw
import math

TILE = 32  # each block is 32x32 pixels
COLS = 10
ROWS = 10
TOTAL = 100

# ── palette ──────────────────────────────────────────────────────────────────
C = {
    # grass / nature
    "grass_top":    (106, 176, 76),
    "grass_mid":    (88,  148, 60),
    "grass_dark":   (60,  110, 40),
    "dirt":         (139, 101, 70),
    "dirt_dark":    (110,  78, 50),
    "dirt_mid":     (122,  88, 60),
    "root":         (90,   60, 35),
    # stone / rock
    "stone":        (130, 130, 140),
    "stone_dark":   (90,   90, 100),
    "stone_mid":    (110, 110, 120),
    "stone_light":  (160, 160, 170),
    "stone_crack":  (70,   70,  80),
    # sand / desert
    "sand":         (220, 195, 140),
    "sand_dark":    (185, 158, 100),
    "sand_mid":     (200, 175, 120),
    # water / ice
    "water":        (60,  140, 200),
    "water_dark":   (40,  100, 160),
    "water_light":  (100, 180, 230),
    "ice":          (180, 220, 240),
    "ice_dark":     (140, 190, 220),
    # wood / forest
    "wood":         (140,  90,  50),
    "wood_dark":    (100,  60,  30),
    "wood_light":   (170, 120,  70),
    "leaf":         (60,  150,  50),
    "leaf_dark":    (40,  110,  35),
    "leaf_light":   (90,  180,  70),
    # dungeon / cave
    "dungeon":      (55,   50,  65),
    "dungeon_mid":  (75,   70,  88),
    "dungeon_light":(100,  90, 115),
    "moss":         (80,  120,  60),
    "moss_dark":    (55,   85,  40),
    # lava / fire
    "lava":         (220,  80,  20),
    "lava_bright":  (255, 140,  30),
    "lava_dark":    (160,  40,   5),
    "ember":        (255, 200,  50),
    "obsidian":     (35,   25,  45),
    "obsidian_shine":(70,  55,  90),
    # fantasy / magic
    "crystal":      (130, 90,  200),
    "crystal_light":(180, 140, 240),
    "crystal_dark": (90,   60, 150),
    "gold":         (220, 180,  50),
    "gold_dark":    (170, 130,  20),
    "gold_mid":     (200, 160,  35),
    "rune":         (80,  200, 200),
    # sky / clouds
    "sky":          (100, 170, 230),
    "sky_dark":     (70,  130, 190),
    "cloud":        (240, 245, 255),
    "cloud_shadow": (210, 215, 230),
    # misc
    "black":        (20,   20,  25),
    "white":        (245, 245, 250),
    "shadow":       (0,    0,   0, 80),
    "trans":        (0,    0,   0,  0),
}

def px(draw, x, y, color):
    """Draw a single 1x1 'pixel' in tile-local coords (scaled 2x for 32px tile)."""
    s = 2  # each logical pixel = 2x2 actual pixels for crisper look
    draw.rectangle([x*s, y*s, x*s+s-1, y*s+s-1], fill=color)

def tile(draw, bg):
    draw.rectangle([0, 0, TILE-1, TILE-1], fill=bg)

def checkerNoise(draw, c1, c2, density=0.25):
    import random
    rng = random.Random(42)
    s = 2
    for py_ in range(16):
        for px_ in range(16):
            if rng.random() < density:
                px(draw, px_, py_, c2)

# ─────────────────────────────────────────────────────────────────────────────
# Block drawing functions  (each receives a fresh RGBA Image 32x32)
# ─────────────────────────────────────────────────────────────────────────────

def draw_grass_top(img):
    d = ImageDraw.Draw(img)
    tile(d, C["dirt"])
    checkerNoise(d, C["dirt"], C["dirt_dark"], 0.2)
    # top 5 rows = grass
    for row in range(5):
        shade = C["grass_top"] if row < 3 else C["grass_mid"]
        d.rectangle([0, row*2, TILE-1, row*2+1], fill=shade)
    # grass tufts
    for x in [2,5,9,13]:
        d.rectangle([x*2, 2, x*2+1, 5], fill=C["grass_dark"])

def draw_grass_mid(img):
    d = ImageDraw.Draw(img)
    tile(d, C["grass_mid"])
    checkerNoise(d, C["grass_mid"], C["grass_dark"], 0.15)
    for x in [1,4,7,11,14]:
        d.rectangle([x*2, 0, x*2+1, 3], fill=C["grass_top"])

def draw_dirt(img):
    d = ImageDraw.Draw(img)
    tile(d, C["dirt"])
    checkerNoise(d, C["dirt"], C["dirt_dark"], 0.3)
    for x in [3,8,12]:
        d.rectangle([x*2, 6*2, x*2+3, 6*2+1], fill=C["dirt_dark"])

def draw_dirt_path(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sand_dark"])
    checkerNoise(d, C["sand_dark"], C["dirt"], 0.35)
    d.rectangle([3*2, 5*2, 12*2, 6*2], fill=C["sand_mid"])

def draw_stone_block(img):
    d = ImageDraw.Draw(img)
    tile(d, C["stone"])
    # mortar lines
    d.rectangle([0, 7*2, TILE-1, 7*2+1], fill=C["stone_dark"])
    d.rectangle([8*2, 0, 8*2+1, 7*2], fill=C["stone_dark"])
    d.rectangle([4*2, 7*2, 4*2+1, TILE-1], fill=C["stone_dark"])
    # highlight top-left
    d.rectangle([0, 0, TILE-1, 1], fill=C["stone_light"])
    d.rectangle([0, 0, 1, TILE-1], fill=C["stone_light"])

def draw_stone_cracked(img):
    d = ImageDraw.Draw(img)
    draw_stone_block(img)
    d2 = ImageDraw.Draw(img)
    # cracks
    d2.line([5*2, 2*2, 7*2, 6*2], fill=C["stone_crack"], width=1)
    d2.line([10*2, 9*2, 12*2, 14*2], fill=C["stone_crack"], width=1)

def draw_stone_mossy(img):
    d = ImageDraw.Draw(img)
    draw_stone_block(img)
    d2 = ImageDraw.Draw(img)
    for x in [1,5,10,13]:
        d2.rectangle([x*2, 0, x*2+3, 4], fill=C["moss"])

def draw_cobblestone(img):
    d = ImageDraw.Draw(img)
    tile(d, C["stone_dark"])
    stones = [(1,1,5,5),(7,1,11,4),(12,2,15,6),(0,6,4,10),(5,6,9,10),(11,7,15,11),(2,11,6,15),(8,11,13,15)]
    for (x1,y1,x2,y2) in stones:
        d.rectangle([x1*2,y1*2,x2*2,y2*2], fill=C["stone"])
        d.rectangle([x1*2,y1*2,x2*2,y1*2+1], fill=C["stone_light"])

def draw_sand(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sand"])
    checkerNoise(d, C["sand"], C["sand_dark"], 0.2)

def draw_sand_dune(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sand"])
    # wavy top
    for x in range(16):
        h = int(2 + 2*math.sin(x*0.8))
        d.rectangle([x*2, 0, x*2+1, h*2], fill=C["sand_dark"])

def draw_sandstone(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sand_mid"])
    for y in [4,9,13]:
        d.rectangle([0, y*2, TILE-1, y*2+1], fill=C["sand_dark"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["sand"])

def draw_water_surface(img):
    d = ImageDraw.Draw(img)
    tile(d, C["water"])
    for x in range(16):
        h = int(1 + 1.5*math.sin(x*0.9))
        d.rectangle([x*2, h*2, x*2+1, h*2+3], fill=C["water_light"])
    d.rectangle([0, 0, TILE-1, 3], fill=C["water_light"])

def draw_water_deep(img):
    d = ImageDraw.Draw(img)
    tile(d, C["water_dark"])
    for x in [2,6,10,13]:
        d.rectangle([x*2, 4*2, x*2+2, 5*2], fill=C["water"])

def draw_water_shallow(img):
    d = ImageDraw.Draw(img)
    tile(d, C["water"])
    checkerNoise(d, C["water"], C["water_light"], 0.15)
    # sandy bottom hint
    for x in [3,8,13]:
        d.rectangle([x*2, 12*2, x*2+4, 13*2], fill=C["sand"])

def draw_ice(img):
    d = ImageDraw.Draw(img)
    tile(d, C["ice"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["white"])
    d.rectangle([0, 0, 1, TILE-1], fill=C["white"])
    checkerNoise(d, C["ice"], C["ice_dark"], 0.1)

def draw_ice_cracked(img):
    d = ImageDraw.Draw(img)
    draw_ice(img)
    d2 = ImageDraw.Draw(img)
    d2.line([3*2, 3*2, 8*2, 10*2], fill=C["water_dark"], width=1)
    d2.line([8*2, 10*2, 14*2, 13*2], fill=C["water_dark"], width=1)

def draw_snow(img):
    d = ImageDraw.Draw(img)
    tile(d, (230, 240, 255))
    checkerNoise(d, (230,240,255), C["white"], 0.25)

def draw_snow_grass(img):
    d = ImageDraw.Draw(img)
    draw_grass_top(img)
    d2 = ImageDraw.Draw(img)
    d2.rectangle([0, 0, TILE-1, 5], fill=(235, 245, 255))
    for x in [2,6,11]:
        d2.rectangle([x*2, 0, x*2+3, 3], fill=C["white"])

def draw_wood_log_h(img):
    d = ImageDraw.Draw(img)
    tile(d, C["wood"])
    d.rectangle([0, 2*2, TILE-1, 13*2], fill=C["wood"])
    d.rectangle([0, 2*2, TILE-1, 3*2], fill=C["wood_light"])
    d.rectangle([0, 12*2, TILE-1, 13*2], fill=C["wood_dark"])
    for x in [2,5,9,13]:
        d.rectangle([x*2, 4*2, x*2+1, 11*2], fill=C["wood_dark"])

def draw_wood_plank(img):
    d = ImageDraw.Draw(img)
    tile(d, C["wood_light"])
    d.rectangle([0, 7*2, TILE-1, 7*2+1], fill=C["wood_dark"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["wood_light"])
    for x in [3,11]:
        d.rectangle([x*2, 1*2, x*2+1, 6*2], fill=C["wood"])
        d.rectangle([x*2, 8*2, x*2+1, 15*2], fill=C["wood"])

def draw_tree_trunk(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([4*2, 0, 11*2, TILE-1], fill=C["wood"])
    d.rectangle([5*2, 0, 6*2, TILE-1], fill=C["wood_light"])
    d.rectangle([9*2, 0, 10*2, TILE-1], fill=C["wood_dark"])
    for y in [3,8,12]:
        d.rectangle([4*2, y*2, 11*2, y*2+1], fill=C["wood_dark"])

def draw_tree_leaves(img):
    d = ImageDraw.Draw(img)
    tile(d, C["leaf"])
    checkerNoise(d, C["leaf"], C["leaf_dark"], 0.3)
    # round shape
    for x in [0,1,14,15]:
        d.rectangle([x*2, 0, x*2+1, TILE-1], fill=(0,0,0,0))
    for y in [0,1,14,15]:
        d.rectangle([0, y*2, TILE-1, y*2+1], fill=(0,0,0,0))

def draw_tree_leaves_dark(img):
    d = ImageDraw.Draw(img)
    tile(d, C["leaf_dark"])
    checkerNoise(d, C["leaf_dark"], C["leaf"], 0.2)

def draw_bush(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.ellipse([2*2, 4*2, 13*2, 14*2], fill=C["leaf"])
    d.ellipse([3*2, 5*2, 12*2, 13*2], fill=C["leaf_light"])
    for x in [4,8]:
        d.rectangle([x*2, 5*2, x*2+2, 7*2], fill=C["leaf_dark"])

def draw_cactus(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([5*2, 0, 10*2, TILE-1], fill=C["grass_dark"])
    d.rectangle([6*2, 0, 9*2, TILE-1], fill=C["grass_mid"])
    d.rectangle([1*2, 5*2, 5*2, 8*2], fill=C["grass_dark"])
    d.rectangle([10*2, 8*2, 14*2, 11*2], fill=C["grass_dark"])

def draw_dungeon_floor(img):
    d = ImageDraw.Draw(img)
    tile(d, C["dungeon"])
    checkerNoise(d, C["dungeon"], C["dungeon_mid"], 0.2)

def draw_dungeon_wall(img):
    d = ImageDraw.Draw(img)
    tile(d, C["dungeon_mid"])
    d.rectangle([0, 7*2, TILE-1, 7*2+1], fill=C["dungeon"])
    d.rectangle([8*2, 0, 8*2+1, 7*2], fill=C["dungeon"])
    d.rectangle([3*2, 7*2, 3*2+1, TILE-1], fill=C["dungeon"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["dungeon_light"])

def draw_dungeon_mossy(img):
    d = ImageDraw.Draw(img)
    draw_dungeon_wall(img)
    d2 = ImageDraw.Draw(img)
    for x in [0,4,9,13]:
        d2.rectangle([x*2, 12*2, x*2+3, TILE-1], fill=C["moss_dark"])
    for x in [1,6,11]:
        d2.rectangle([x*2, 13*2, x*2+2, TILE-1], fill=C["moss"])

def draw_lava(img):
    d = ImageDraw.Draw(img)
    tile(d, C["lava"])
    for x in range(16):
        h = int(2 + 2*abs(math.sin(x*0.7)))
        d.rectangle([x*2, h*2, x*2+1, h*2+3], fill=C["lava_bright"])
    checkerNoise(d, C["lava"], C["ember"], 0.1)

def draw_lava_rock(img):
    d = ImageDraw.Draw(img)
    tile(d, C["obsidian"])
    checkerNoise(d, C["obsidian"], C["lava_dark"], 0.2)
    for x in [2,8,12]:
        d.rectangle([x*2, 5*2, x*2+2, 6*2], fill=C["lava"])

def draw_obsidian(img):
    d = ImageDraw.Draw(img)
    tile(d, C["obsidian"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["obsidian_shine"])
    d.rectangle([0, 0, 1, TILE-1], fill=C["obsidian_shine"])
    checkerNoise(d, C["obsidian"], C["obsidian_shine"], 0.08)

def draw_obsidian_cracked(img):
    d = ImageDraw.Draw(img)
    draw_obsidian(img)
    d2 = ImageDraw.Draw(img)
    d2.line([2*2, 1*2, 7*2, 8*2], fill=C["lava"], width=1)
    d2.line([7*2, 8*2, 4*2, 14*2], fill=C["lava"], width=1)

def draw_crystal_blue(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    # crystal shape
    pts = [8*2,0, 14*2,6*2, 11*2,TILE-1, 5*2,TILE-1, 2*2,6*2]
    d.polygon(pts, fill=C["crystal"])
    d.line([8*2,0, 14*2,6*2], fill=C["crystal_light"], width=2)
    d.line([8*2,0, 2*2,6*2], fill=C["crystal_dark"], width=1)

def draw_crystal_purple(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    pts = [8*2,0, 13*2,8*2, 8*2,TILE-1, 3*2,8*2]
    d.polygon(pts, fill=(110,70,170))
    d.line([8*2,0, 13*2,8*2], fill=(160,120,220), width=2)

def draw_crystal_green(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    pts = [8*2,0, 15*2,7*2, 10*2,TILE-1, 6*2,TILE-1, 1*2,7*2]
    d.polygon(pts, fill=(60,160,100))
    d.line([8*2,0, 15*2,7*2], fill=(100,210,140), width=2)

def draw_gold_block(img):
    d = ImageDraw.Draw(img)
    tile(d, C["gold"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["ember"])
    d.rectangle([0, 0, 1, TILE-1], fill=C["ember"])
    d.rectangle([0, TILE-2, TILE-1, TILE-1], fill=C["gold_dark"])
    d.rectangle([TILE-2, 0, TILE-1, TILE-1], fill=C["gold_dark"])
    # coin shine
    d.ellipse([4*2, 4*2, 11*2, 11*2], outline=C["ember"], width=1)

def draw_gold_ore(img):
    d = ImageDraw.Draw(img)
    draw_stone_block(img)
    d2 = ImageDraw.Draw(img)
    for (x,y) in [(2,2),(7,5),(11,2),(4,10),(12,11)]:
        d2.rectangle([x*2, y*2, x*2+3, y*2+3], fill=C["gold"])

def draw_rune_stone(img):
    d = ImageDraw.Draw(img)
    tile(d, C["dungeon_mid"])
    d2 = ImageDraw.Draw(img)
    d2.rectangle([0, 0, TILE-1, 1], fill=C["rune"])
    d2.rectangle([0, TILE-2, TILE-1, TILE-1], fill=C["rune"])
    d2.line([8*2, 2*2, 8*2, 13*2], fill=C["rune"], width=2)
    d2.line([3*2, 7*2, 12*2, 7*2], fill=C["rune"], width=2)
    d2.line([4*2, 3*2, 12*2, 12*2], fill=C["rune"], width=1)

def draw_magic_floor(img):
    d = ImageDraw.Draw(img)
    tile(d, (30, 20, 50))
    for (x,y) in [(3,3),(7,7),(11,3),(3,11),(11,11),(7,13)]:
        d.ellipse([x*2-2, y*2-2, x*2+2, y*2+2], fill=C["rune"])
    d.line([3*2, 3*2, 11*2, 3*2], fill=C["rune"], width=1)
    d.line([3*2, 3*2, 3*2, 11*2], fill=C["rune"], width=1)
    d.line([11*2, 3*2, 11*2, 11*2], fill=C["rune"], width=1)
    d.line([3*2, 11*2, 11*2, 11*2], fill=C["rune"], width=1)
    d.line([7*2, 3*2, 11*2, 11*2], fill=C["crystal"], width=1)
    d.line([7*2, 3*2, 3*2, 11*2], fill=C["crystal"], width=1)

def draw_portal_frame(img):
    d = ImageDraw.Draw(img)
    tile(d, C["obsidian"])
    d2 = ImageDraw.Draw(img)
    d2.rectangle([0, 0, TILE-1, 3], fill=C["obsidian"])
    d2.rectangle([0, TILE-4, TILE-1, TILE-1], fill=C["obsidian"])
    d2.rectangle([0, 0, 3, TILE-1], fill=C["obsidian"])
    d2.rectangle([TILE-4, 0, TILE-1, TILE-1], fill=C["obsidian"])
    d2.rectangle([4, 4, TILE-5, TILE-5], fill=(80, 0, 120))
    d2.rectangle([6, 6, TILE-7, TILE-7], fill=(120, 30, 180))
    checkerNoise(d2, (80,0,120), (130,50,200), 0.2)

def draw_brick_red(img):
    d = ImageDraw.Draw(img)
    tile(d, (160, 80, 60))
    d.rectangle([0, 5*2, TILE-1, 5*2+1], fill=(120,60,45))
    d.rectangle([0, 10*2, TILE-1, 10*2+1], fill=(120,60,45))
    d.rectangle([4*2, 0, 4*2+1, 5*2], fill=(120,60,45))
    d.rectangle([12*2, 0, 12*2+1, 5*2], fill=(120,60,45))
    d.rectangle([8*2, 5*2, 8*2+1, 10*2], fill=(120,60,45))
    d.rectangle([0*2, 10*2, 0*2+1, TILE-1], fill=(120,60,45))
    d.rectangle([10*2, 10*2, 10*2+1, TILE-1], fill=(120,60,45))
    d.rectangle([0, 0, TILE-1, 1], fill=(200,120,90))

def draw_brick_dark(img):
    d = ImageDraw.Draw(img)
    tile(d, (80, 50, 40))
    d2 = ImageDraw.Draw(img)
    for y in [5, 10]:
        d2.rectangle([0, y*2, TILE-1, y*2+1], fill=(50,30,20))
    for x in [4, 12]:
        d2.rectangle([x*2, 0, x*2+1, 5*2], fill=(50,30,20))
    for x in [8]:
        d2.rectangle([x*2, 5*2, x*2+1, 10*2], fill=(50,30,20))

def draw_castle_wall(img):
    d = ImageDraw.Draw(img)
    draw_stone_block(img)
    d2 = ImageDraw.Draw(img)
    # battlement notch at top
    d2.rectangle([4*2, 0, 11*2, 4*2], fill=C["stone_dark"])

def draw_castle_floor(img):
    d = ImageDraw.Draw(img)
    tile(d, C["stone_mid"])
    d2 = ImageDraw.Draw(img)
    d2.rectangle([0, 7*2, TILE-1, 7*2+1], fill=C["stone"])
    d2.rectangle([8*2, 0, 8*2+1, TILE-1], fill=C["stone"])

def draw_gravel(img):
    d = ImageDraw.Draw(img)
    tile(d, (120,115,110))
    for (x,y) in [(1,2),(5,1),(9,3),(13,1),(2,6),(7,5),(11,7),(3,10),(8,11),(12,9),(1,13),(6,14),(14,13)]:
        d.ellipse([x*2-2,y*2-2,x*2+4,y*2+4], fill=(100,95,90))
        d.ellipse([x*2-1,y*2-1,x*2+2,y*2+2], fill=(140,135,130))

def draw_clay(img):
    d = ImageDraw.Draw(img)
    tile(d, (160, 130, 120))
    checkerNoise(d, (160,130,120), (140,110,100), 0.25)

def draw_mud(img):
    d = ImageDraw.Draw(img)
    tile(d, (100, 80, 60))
    for x in range(16):
        h = int(1 + abs(math.sin(x*1.1)))
        d.rectangle([x*2, h*2, x*2+1, h*2+1], fill=(80,65,45))

def draw_hay(img):
    d = ImageDraw.Draw(img)
    tile(d, (210, 180, 90))
    for y in range(16):
        if y % 2 == 0:
            d.rectangle([0, y*2, TILE-1, y*2+1], fill=(190,160,70))

def draw_mushroom_top(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.ellipse([1*2, 1*2, 14*2, 11*2], fill=(180,50,50))
    for (x,y) in [(4,3),(8,2),(11,4),(6,7),(9,6)]:
        d.ellipse([x*2-2,y*2-2,x*2+2,y*2+2], fill=(230,200,180))
    d.rectangle([5*2, 10*2, 10*2, TILE-1], fill=(220,190,170))

def draw_mushroom_stem(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([5*2, 0, 10*2, 12*2], fill=(220,190,170))
    d.rectangle([4*2, 10*2, 11*2, 12*2], fill=(200,170,150))

def draw_flower_patch(img):
    d = ImageDraw.Draw(img)
    draw_grass_top(img)
    d2 = ImageDraw.Draw(img)
    for (x,y,col) in [(2,4,(230,80,80)),(8,3,(230,200,50)),(13,5,(150,100,220))]:
        d2.ellipse([x*2-2,y*2-2,x*2+2,y*2+2], fill=col)
        d2.ellipse([x*2-1,y*2-1,x*2+1,y*2+1], fill=(240,230,50))

def draw_vines(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    for x in [2,6,10,14]:
        for y in range(0, 16, 2):
            shade = C["leaf"] if y%4==0 else C["leaf_dark"]
            d.ellipse([x*2-2,y*2,x*2+4,y*2+4], fill=shade)

def draw_chain(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    for y in range(8):
        d.rectangle([6*2, y*4, 9*2, y*4+1], fill=C["stone_light"])
        d.rectangle([5*2, y*4+2, 10*2, y*4+3], fill=C["stone_mid"])

def draw_ladder(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([3*2, 0, 4*2, TILE-1], fill=C["wood"])
    d.rectangle([11*2, 0, 12*2, TILE-1], fill=C["wood"])
    for y in [2,5,8,11,14]:
        d.rectangle([3*2, y*2, 12*2, y*2+1], fill=C["wood_light"])

def draw_door_wood(img):
    d = ImageDraw.Draw(img)
    tile(d, C["wood"])
    d.rectangle([1*2, 0, 14*2, TILE-1], fill=C["wood_light"])
    d.rectangle([1*2, 0, 14*2, 1], fill=C["wood"])
    d.rectangle([1*2, 0, 2*2, TILE-1], fill=C["wood"])
    d.rectangle([13*2, 0, 14*2, TILE-1], fill=C["wood"])
    d.rectangle([1*2, 7*2, 14*2, 7*2+1], fill=C["wood"])
    d.ellipse([10*2, 6*2, 12*2, 8*2], fill=C["gold"])

def draw_window(img):
    d = ImageDraw.Draw(img)
    draw_stone_block(img)
    d2 = ImageDraw.Draw(img)
    d2.rectangle([3*2, 2*2, 12*2, 13*2], fill=C["water_light"])
    d2.rectangle([7*2, 2*2, 8*2, 13*2], fill=C["stone"])
    d2.rectangle([3*2, 7*2, 12*2, 8*2], fill=C["stone"])

def draw_torch(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([7*2, 5*2, 8*2, 13*2], fill=C["wood"])
    # flame
    d.ellipse([5*2, 1*2, 10*2, 7*2], fill=C["lava"])
    d.ellipse([6*2, 2*2, 9*2, 6*2], fill=C["ember"])
    d.ellipse([7*2, 2*2, 8*2, 4*2], fill=C["white"])

def draw_chest(img):
    d = ImageDraw.Draw(img)
    tile(d, C["wood"])
    d.rectangle([1*2, 4*2, 14*2, 14*2], fill=C["wood_light"])
    d.rectangle([1*2, 4*2, 14*2, 8*2], fill=C["wood"])
    d.rectangle([1*2, 4*2, 14*2, 4*2+1], fill=C["wood_light"])
    d.ellipse([6*2, 5*2, 9*2, 8*2], fill=C["gold"])
    d.rectangle([1*2, 8*2, 14*2, 8*2+1], fill=C["gold_dark"])

def draw_spike(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([0, 12*2, TILE-1, TILE-1], fill=C["stone_dark"])
    for x in [1,5,9,13]:
        pts = [x*2,12*2, x*2+3,12*2, x*2+1,1*2]
        d.polygon(pts, fill=C["stone"])
        d.line([x*2,12*2, x*2+1,1*2], fill=C["stone_light"], width=1)

def draw_pressure_plate(img):
    d = ImageDraw.Draw(img)
    tile(d, C["stone_dark"])
    d.rectangle([2*2, 5*2, 13*2, 8*2], fill=C["stone"])
    d.rectangle([2*2, 5*2, 13*2, 5*2+1], fill=C["stone_light"])

def draw_chest_open(img):
    d = ImageDraw.Draw(img)
    draw_chest(img)
    d2 = ImageDraw.Draw(img)
    # open lid hint
    d2.rectangle([1*2, 1*2, 14*2, 5*2], fill=C["wood"])
    d2.rectangle([1*2, 4*2, 14*2, 5*2+1], fill=C["gold"])
    d2.ellipse([5*2, 4*2, 10*2, 7*2], fill=C["ember"])

def draw_barrel(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.ellipse([2*2, 0, 13*2, 4*2], fill=C["wood"])
    d.rectangle([2*2, 2*2, 13*2, 13*2], fill=C["wood_light"])
    d.ellipse([2*2, 11*2, 13*2, 15*2], fill=C["wood"])
    for y in [4,8,11]:
        d.rectangle([2*2, y*2, 13*2, y*2+1], fill=C["gold_dark"])

def draw_bookshelf(img):
    d = ImageDraw.Draw(img)
    draw_wood_plank(img)
    d2 = ImageDraw.Draw(img)
    colors = [(180,60,60),(60,100,180),(60,160,80),(200,160,40),(140,60,160)]
    for i,col in enumerate(colors):
        x = 1 + i*3
        d2.rectangle([x*2, 1*2, (x+2)*2, 6*2], fill=col)
    colors2 = [(160,80,40),(80,140,160),(190,190,50),(100,80,170),(170,90,90)]
    for i,col in enumerate(colors2):
        x = 1 + i*3
        d2.rectangle([x*2, 9*2, (x+2)*2, 14*2], fill=col)

def draw_trapdoor(img):
    d = ImageDraw.Draw(img)
    tile(d, C["wood"])
    d.rectangle([1*2, 1*2, 14*2, 14*2], fill=C["wood_light"])
    d.rectangle([1*2, 7*2, 14*2, 7*2+1], fill=C["wood"])
    d.rectangle([7*2, 1*2, 7*2+1, 14*2], fill=C["wood"])
    d.ellipse([3*2, 3*2, 5*2, 5*2], fill=C["gold"])
    d.ellipse([10*2, 10*2, 12*2, 12*2], fill=C["gold"])

def draw_fence(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([4*2, 0, 5*2, TILE-1], fill=C["wood"])
    d.rectangle([10*2, 0, 11*2, TILE-1], fill=C["wood"])
    d.rectangle([0, 3*2, TILE-1, 4*2], fill=C["wood_light"])
    d.rectangle([0, 9*2, TILE-1, 10*2], fill=C["wood_light"])

def draw_pillar_base(img):
    d = ImageDraw.Draw(img)
    tile(d, C["stone_mid"])
    d.rectangle([0, 0, TILE-1, 3], fill=C["stone_light"])
    d.rectangle([0, TILE-4, TILE-1, TILE-1], fill=C["stone_dark"])
    d.rectangle([2*2, 3, (TILE-4), TILE-5], fill=C["stone"])

def draw_pillar_mid(img):
    d = ImageDraw.Draw(img)
    tile(d, C["stone"])
    d.rectangle([2*2, 0, TILE-5, TILE-1], fill=C["stone_mid"])
    d.rectangle([3*2, 0, 4*2, TILE-1], fill=C["stone_light"])

def draw_sky_block(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sky"])
    checkerNoise(d, C["sky"], C["sky_dark"], 0.05)

def draw_cloud_block(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sky"])
    d.ellipse([1*2, 2*2, 14*2, 13*2], fill=C["cloud"])
    d.ellipse([3*2, 1*2, 11*2, 6*2], fill=C["white"])
    d.rectangle([1*2, 7*2, 14*2, 13*2], fill=C["cloud"])

def draw_cloud_edge_left(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sky"])
    d.ellipse([4*2, 2*2, 16*2, 13*2], fill=C["cloud"])
    d.rectangle([8*2, 7*2, TILE-1, 13*2], fill=C["cloud"])

def draw_cloud_edge_right(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sky"])
    d.ellipse([0, 2*2, 11*2, 13*2], fill=C["cloud"])
    d.rectangle([0, 7*2, 7*2, 13*2], fill=C["cloud"])

def draw_star_sky(img):
    d = ImageDraw.Draw(img)
    tile(d, (15, 10, 35))
    for (x,y) in [(2,1),(6,3),(11,1),(14,4),(3,8),(8,6),(13,9),(1,12),(5,14),(10,12),(15,13)]:
        d.rectangle([x*2, y*2, x*2+1, y*2+1], fill=C["white"])

def draw_moon_block(img):
    d = ImageDraw.Draw(img)
    tile(d, (15,10,35))
    d.ellipse([2*2, 2*2, 13*2, 13*2], fill=(230,220,190))
    d.ellipse([5*2, 1*2, 13*2, 9*2], fill=(15,10,35))

def draw_sun_block(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sky"])
    d.ellipse([3*2, 3*2, 12*2, 12*2], fill=C["ember"])
    d.ellipse([4*2, 4*2, 11*2, 11*2], fill=C["white"])
    for angle in range(0,360,45):
        rad = math.radians(angle)
        sx = int(8 + 6*math.cos(rad))
        sy = int(8 + 6*math.sin(rad))
        ex = int(8 + 8*math.cos(rad))
        ey = int(8 + 8*math.sin(rad))
        d.line([sx*2,sy*2,ex*2,ey*2], fill=C["ember"], width=2)

def draw_rainbow(img):
    d = ImageDraw.Draw(img)
    tile(d, C["sky"])
    colors = [(220,60,60),(220,150,50),(220,220,50),(80,200,80),(60,120,220),(140,60,200)]
    for i,col in enumerate(colors):
        r = (5+i)*2
        d.arc([int(TILE/2)-r, int(TILE/2)-r, int(TILE/2)+r, int(TILE/2)+r], 180, 360, fill=col, width=2)

def draw_fog(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    fog = Image.new("RGBA", (TILE,TILE), (200,210,220,120))
    img.paste(fog, (0,0), fog)
    d2 = ImageDraw.Draw(img)
    for x in [1,5,10,13]:
        d2.ellipse([x*2-3,4*2,x*2+6,10*2], fill=(220,225,230,100))

def draw_shadow_block(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    shadow = Image.new("RGBA", (TILE,TILE), (0,0,0,100))
    img.paste(shadow, (0,0), shadow)

def draw_empty(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))

def draw_platform_wood(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([0, 0, TILE-1, 7], fill=C["wood"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["wood_light"])
    d.rectangle([0, 6, TILE-1, 7], fill=C["wood_dark"])
    for x in [4,12]:
        d.rectangle([x*2, 0, x*2+1, 7], fill=C["wood_dark"])

def draw_platform_stone(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([0, 0, TILE-1, 7], fill=C["stone"])
    d.rectangle([0, 0, TILE-1, 1], fill=C["stone_light"])
    d.rectangle([0, 6, TILE-1, 7], fill=C["stone_dark"])

def draw_slope_grass_l(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    for x in range(16):
        top = 15 - x
        d.rectangle([x*2, top*2, x*2+1, TILE-1], fill=C["dirt"])
        d.rectangle([x*2, top*2, x*2+1, top*2+3], fill=C["grass_top"])

def draw_slope_grass_r(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    for x in range(16):
        top = x
        d.rectangle([x*2, top*2, x*2+1, TILE-1], fill=C["dirt"])
        d.rectangle([x*2, top*2, x*2+1, top*2+3], fill=C["grass_top"])

def draw_coral(img):
    d = ImageDraw.Draw(img)
    tile(d, C["water_dark"])
    d.rectangle([6*2, 4*2, 9*2, TILE-1], fill=(200,80,120))
    d.rectangle([3*2, 8*2, 6*2, TILE-1], fill=(240,120,60))
    d.rectangle([9*2, 7*2, 12*2, TILE-1], fill=(200,80,120))
    d.ellipse([5*2,3*2,10*2,7*2], fill=(240,80,140))

def draw_seaweed(img):
    d = ImageDraw.Draw(img)
    tile(d, C["water_dark"])
    for y in range(16):
        x = int(7 + 2*math.sin(y*0.7))
        d.rectangle([x*2, y*2, x*2+2, y*2+2], fill=C["leaf"])
    for y in range(16):
        x = int(10 + 2*math.sin(y*0.9+1))
        d.rectangle([x*2, y*2, x*2+2, y*2+2], fill=C["leaf_dark"])

def draw_crate(img):
    d = ImageDraw.Draw(img)
    tile(d, C["wood_light"])
    d.rectangle([0,0,TILE-1,1], fill=C["wood"])
    d.rectangle([0,TILE-2,TILE-1,TILE-1], fill=C["wood"])
    d.rectangle([0,0,1,TILE-1], fill=C["wood"])
    d.rectangle([TILE-2,0,TILE-1,TILE-1], fill=C["wood"])
    d.line([0,0,TILE-1,TILE-1], fill=C["wood"], width=2)
    d.line([TILE-1,0,0,TILE-1], fill=C["wood"], width=2)

def draw_bone_block(img):
    d = ImageDraw.Draw(img)
    tile(d, (220,215,200))
    for y in [4,9,13]:
        d.rectangle([0, y*2, TILE-1, y*2+1], fill=(190,185,170))
    d.rectangle([0, 0, TILE-1, 1], fill=(235,230,220))
    checkerNoise(d, (220,215,200), (200,195,180), 0.1)

def draw_altar(img):
    d = ImageDraw.Draw(img)
    tile(d, C["stone_dark"])
    d.rectangle([1*2, 2*2, 14*2, 13*2], fill=C["stone"])
    d.rectangle([1*2, 2*2, 14*2, 3*2], fill=C["stone_light"])
    d.rectangle([3*2, 13*2, 12*2, 15*2], fill=C["stone_dark"])
    d.ellipse([5*2, 4*2, 10*2, 9*2], fill=C["rune"])
    d.ellipse([6*2, 5*2, 9*2, 8*2], fill=C["crystal"])

def draw_cauldron(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([2*2, 7*2, 13*2, 14*2], fill=(50,50,60))
    d.ellipse([1*2, 6*2, 14*2, 11*2], fill=(60,60,75))
    d.ellipse([3*2, 4*2, 12*2, 8*2], fill=(80,180,100))
    d.ellipse([4*2, 5*2, 11*2, 8*2], fill=(100,210,120))
    d.rectangle([0, 13*2, TILE-1, TILE-1], fill=(50,50,60))

def draw_banner_red(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([4*2, 0, 11*2, 1*2], fill=C["wood_dark"])
    d.polygon([4*2,2*2, 11*2,2*2, 11*2,13*2, 7*2,15*2, 4*2,13*2], fill=(180,40,40))
    d.ellipse([6*2,6*2,9*2,9*2], fill=C["gold"])

def draw_banner_blue(img):
    d = ImageDraw.Draw(img)
    tile(d, (0,0,0,0))
    d.rectangle([4*2, 0, 11*2, 1*2], fill=C["wood_dark"])
    d.polygon([4*2,2*2, 11*2,2*2, 11*2,13*2, 7*2,15*2, 4*2,13*2], fill=(40,80,180))
    d.ellipse([6*2,6*2,9*2,9*2], fill=C["gold"])

# ── block catalog ─────────────────────────────────────────────────────────────
BLOCKS = [
    # TERRAIN - GRASS & EARTH  (0-9)
    ("Grass Top",        draw_grass_top),
    ("Grass Mid",        draw_grass_mid),
    ("Dirt",             draw_dirt),
    ("Dirt Path",        draw_dirt_path),
    ("Slope Grass L",    draw_slope_grass_l),
    ("Slope Grass R",    draw_slope_grass_r),
    ("Clay",             draw_clay),
    ("Mud",              draw_mud),
    ("Gravel",           draw_gravel),
    ("Hay",              draw_hay),
    # TERRAIN - STONE  (10-19)
    ("Stone Block",      draw_stone_block),
    ("Stone Cracked",    draw_stone_cracked),
    ("Stone Mossy",      draw_stone_mossy),
    ("Cobblestone",      draw_cobblestone),
    ("Castle Wall",      draw_castle_wall),
    ("Castle Floor",     draw_castle_floor),
    ("Pillar Base",      draw_pillar_base),
    ("Pillar Mid",       draw_pillar_mid),
    ("Brick Red",        draw_brick_red),
    ("Brick Dark",       draw_brick_dark),
    # TERRAIN - SAND & DESERT  (20-24)
    ("Sand",             draw_sand),
    ("Sand Dune",        draw_sand_dune),
    ("Sandstone",        draw_sandstone),
    ("Cactus",           draw_cactus),
    ("Bone Block",       draw_bone_block),
    # TERRAIN - WATER & ICE  (25-34)
    ("Water Surface",    draw_water_surface),
    ("Water Deep",       draw_water_deep),
    ("Water Shallow",    draw_water_shallow),
    ("Ice",              draw_ice),
    ("Ice Cracked",      draw_ice_cracked),
    ("Snow",             draw_snow),
    ("Snow Grass",       draw_snow_grass),
    ("Coral",            draw_coral),
    ("Seaweed",          draw_seaweed),
    ("Fog",              draw_fog),
    # NATURE  (35-46)
    ("Wood Log H",       draw_wood_log_h),
    ("Wood Plank",       draw_wood_plank),
    ("Tree Trunk",       draw_tree_trunk),
    ("Tree Leaves",      draw_tree_leaves),
    ("Tree Leaves Dark", draw_tree_leaves_dark),
    ("Bush",             draw_bush),
    ("Flower Patch",     draw_flower_patch),
    ("Vines",            draw_vines),
    ("Mushroom Top",     draw_mushroom_top),
    ("Mushroom Stem",    draw_mushroom_stem),
    ("Platform Wood",    draw_platform_wood),
    ("Platform Stone",   draw_platform_stone),
    # DUNGEON / CAVE  (47-54)
    ("Dungeon Floor",    draw_dungeon_floor),
    ("Dungeon Wall",     draw_dungeon_wall),
    ("Dungeon Mossy",    draw_dungeon_mossy),
    ("Lava",             draw_lava),
    ("Lava Rock",        draw_lava_rock),
    ("Obsidian",         draw_obsidian),
    ("Obsidian Cracked", draw_obsidian_cracked),
    ("Spike",            draw_spike),
    # FANTASY / MAGIC  (55-66)
    ("Crystal Blue",     draw_crystal_blue),
    ("Crystal Purple",   draw_crystal_purple),
    ("Crystal Green",    draw_crystal_green),
    ("Gold Block",       draw_gold_block),
    ("Gold Ore",         draw_gold_ore),
    ("Rune Stone",       draw_rune_stone),
    ("Magic Floor",      draw_magic_floor),
    ("Portal Frame",     draw_portal_frame),
    ("Altar",            draw_altar),
    ("Cauldron",         draw_cauldron),
    ("Banner Red",       draw_banner_red),
    ("Banner Blue",      draw_banner_blue),
    # SKY / BACKGROUND  (67-75)
    ("Sky",              draw_sky_block),
    ("Cloud",            draw_cloud_block),
    ("Cloud Left",       draw_cloud_edge_left),
    ("Cloud Right",      draw_cloud_edge_right),
    ("Star Sky",         draw_star_sky),
    ("Moon",             draw_moon_block),
    ("Sun",              draw_sun_block),
    ("Rainbow",          draw_rainbow),
    ("Shadow",           draw_shadow_block),
    # OBJECTS / PROPS  (76-89)
    ("Chest Closed",     draw_chest),
    ("Chest Open",       draw_chest_open),
    ("Barrel",           draw_barrel),
    ("Crate",            draw_crate),
    ("Bookshelf",        draw_bookshelf),
    ("Door Wood",        draw_door_wood),
    ("Window",           draw_window),
    ("Torch",            draw_torch),
    ("Trapdoor",         draw_trapdoor),
    ("Fence",            draw_fence),
    ("Ladder",           draw_ladder),
    ("Chain",            draw_chain),
    ("Pressure Plate",   draw_pressure_plate),
    ("Empty / Air",      draw_empty),
    # EXTRA UTILITY (90-99)
    ("Dirt Dark",        lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["dirt_dark"]) or None)),
    ("Stone Light",      lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["stone_light"]) or None)),
    ("Stone Dark",       lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["stone_dark"]) or None)),
    ("Leaf Solid",       lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["leaf"]) or None)),
    ("Wood Solid",       lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["wood"]) or None)),
    ("Crystal Solid",    lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["crystal"]) or None)),
    ("Lava Solid",       lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["lava"]) or None)),
    ("Gold Solid",       lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["gold"]) or None)),
    ("Obsidian Solid",   lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["obsidian"]) or None)),
    ("Dungeon Solid",    lambda img: (ImageDraw.Draw(img).rectangle([0,0,TILE-1,TILE-1],fill=C["dungeon"]) or None)),
]

assert len(BLOCKS) == 100, f"Got {len(BLOCKS)} blocks"

# ── render sprite sheet ───────────────────────────────────────────────────────
SHEET_W = COLS * TILE
SHEET_H = ROWS * TILE
sheet = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))

tiles = []
for idx, (name, fn) in enumerate(BLOCKS):
    img = Image.new("RGBA", (TILE, TILE), (0, 0, 0, 0))
    fn(img)
    tiles.append(img)
    row, col = divmod(idx, COLS)
    sheet.paste(img, (col * TILE, row * TILE), img)

sheet.save("/Users/jannn/heyhihallo/PRE/Terra-Tower/fantasy_sprite_sheet.png")
print("Sprite sheet saved.")

# ── render reference sheet (labelled grid) ────────────────────────────────────
from PIL import ImageFont

CELL_W, CELL_H = 80, 60
REF_COLS = 10
REF_ROWS = math.ceil(100 / REF_COLS)
ref = Image.new("RGB", (REF_COLS*CELL_W, REF_ROWS*CELL_H + 50), (30, 25, 40))
rd = ImageDraw.Draw(ref)

# title
rd.rectangle([0,0,REF_COLS*CELL_W,44], fill=(20,15,30))
rd.text((REF_COLS*CELL_W//2, 6), "Fantasy Block Set — 100 Tiles (32×32 px)", fill=(200,180,255), anchor="mt")
rd.text((REF_COLS*CELL_W//2, 26), "Sprite sheet: row × 10 cols  |  ID = row*10 + col", fill=(150,140,180), anchor="mt")

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
except:
    font = ImageFont.load_default()
    title_font = font

rd.text((REF_COLS*CELL_W//2, 6), "Fantasy Block Set — 100 Tiles (32×32 px)", font=title_font, fill=(200,180,255), anchor="mt")
rd.text((REF_COLS*CELL_W//2, 26), "Sprite sheet: row × 10 cols  |  ID = row*10 + col", font=font, fill=(150,140,180), anchor="mt")

CHECKER = [(50,45,60),(60,55,70)]
for idx, (name, _) in enumerate(BLOCKS):
    row, col = divmod(idx, REF_COLS)
    ox = col * CELL_W
    oy = 50 + row * CELL_H

    # checkerboard bg
    for cy in range(2):
        for cx in range(2):
            bg = CHECKER[(cx+cy)%2]
            rd.rectangle([ox+cx*CELL_W//2, oy+cy*CELL_H//2,
                           ox+(cx+1)*CELL_W//2-1, oy+(cy+1)*CELL_H//2-1], fill=bg)

    # tile (scaled 2x for visibility)
    scaled = tiles[idx].resize((TILE*2, TILE*2), Image.NEAREST)
    ref.paste(scaled, (ox + (CELL_W - TILE*2)//2, oy + 2), scaled)

    # id badge
    rd.rectangle([ox+1, oy+1, ox+16, oy+10], fill=(20,15,30))
    rd.text((ox+2, oy+1), f"{idx:02d}", font=font, fill=(180,180,200))

    # name
    name_y = oy + CELL_H - 11
    rd.text((ox + CELL_W//2, name_y), name, font=font, fill=(200,200,220), anchor="mt")

    # grid border
    rd.rectangle([ox, oy, ox+CELL_W-1, oy+CELL_H-1], outline=(80,70,100), width=1)

ref.save("/Users/jannn/heyhihallo/PRE/Terra-Tower/fantasy_block_reference.png")
print("Reference sheet saved.")

# ── export individual tiles ───────────────────────────────────────────────────
import os
os.makedirs("/Users/jannn/heyhihallo/PRE/Terra-Tower", exist_ok=True)
for idx, (name, _) in enumerate(BLOCKS):
    safe = name.lower().replace(" ","_").replace("/","_")
    tiles[idx].save(f"/Users/jannn/heyhihallo/PRE/Terra-Tower/{idx:02d}_{safe}.png")
print("Individual tiles saved.")
print("Done!")
