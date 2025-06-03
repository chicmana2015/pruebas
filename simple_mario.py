import os
import pygame
import sys
import urllib.request

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
FPS = 60
GRAVITY = 0.5
JUMP_POWER = 10

SPRITE_URL = "https://raw.githubusercontent.com/mx0c/super-mario-python/master/img/characters.gif"
SPRITE_FILE = "characters.gif"

LEVELS = [
    [
        "....................",
        "....................",
        "....................",
        "....................",
        "....................",
        "......XXX...........",
        "....................",
        "............XXXX....",
        "....................",
        "..................F.",
        "....................",
        "XXXXXXXXXXXXXXXXXXXX",
        "....................",
        "....................",
        "....................",
    ],
    [
        "....................",
        "....................",
        "............XXX.....",
        "....................",
        ".......XXX..........",
        "....................",
        "..................F.",
        ".....XXXXXX.........",
        "....................",
        ".........XXXXXX.....",
        "....................",
        "XXXXXXXXXXXXXXXXXXXX",
        "....................",
        "....................",
        "....................",
    ],
    [
        "....................",
        "....................",
        ".....XXX............",
        "....................",
        "............XXX.....",
        "....................",
        "....................",
        "......XXXXX.........",
        "....................",
        "..................F.",
        "....................",
        "XXXXXXXXXXXXXX......",
        "....................",
        "....................",
        "XXXXXXXXXXXXXXXXXXXX",
    ]
]


def download_sprite():
    if not os.path.exists(SPRITE_FILE):
        try:
            print("Downloading sprite sheet...")
            urllib.request.urlretrieve(SPRITE_URL, SPRITE_FILE)
        except Exception as e:
            print("Failed to download sprite sheet:", e)


def load_player_images(sheet):
    coords = {
        "idle": (276, 44, 16, 16),
        "run1": (290, 44, 16, 16),
        "run2": (304, 44, 16, 16),
        "run3": (321, 44, 16, 16),
        "jump": (355, 44, 16, 16),
    }
    images = {}
    for key, (x, y, w, h) in coords.items():
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.blit(sheet, (0, 0), (x, y, w, h))
        images[key] = pygame.transform.scale(surf, (w * 2, h * 2))
    return images


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.image = self.images["idle"]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False
        self.anim_index = 0

    def update(self, keys, tiles):
        speed = 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.anim_index = (self.anim_index + 0.2) % 3
            self.image = self.images[f"run{int(self.anim_index)+1}"]
        else:
            self.image = self.images["idle"]

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_POWER


class Level:
    def __init__(self, data):
        self.tiles = []
        self.goal_rect = None
        for row_index, row in enumerate(data):
            for col_index, char in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if char == 'X':
                    self.tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif char == 'F':
                    self.goal_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        for tile in self.tiles:
            pygame.draw.rect(screen, (139, 69, 19), tile)
        if self.goal_rect:
            pygame.draw.rect(screen, (255, 0, 0), self.goal_rect)


def main():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    pygame.init()
    download_sprite()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Mario Levels")
    clock = pygame.time.Clock()

    sheet = pygame.image.load(SPRITE_FILE).convert_alpha()
    images = load_player_images(sheet)

    current_level = 0
    level = Level(LEVELS[current_level])
    player = Player(40, HEIGHT - TILE_SIZE*3, images)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        player.update(keys, level.tiles)

        if level.goal_rect and player.rect.colliderect(level.goal_rect):
            current_level += 1
            if current_level >= len(LEVELS):
                print("Congratulations! You finished all levels.")
                running = False
            else:
                level = Level(LEVELS[current_level])
                player.rect.topleft = (40, HEIGHT - TILE_SIZE*3)
                player.vel_y = 0

        screen.fill((92, 148, 252))
        level.draw(screen)
        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
