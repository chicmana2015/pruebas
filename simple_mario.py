import pygame
import sys

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
JUMP_POWER = 10

class Player:
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 100))
        self.vel_y = 0
        self.on_ground = False

    def update(self, keys):
        speed = 5
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_POWER
            self.on_ground = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Mario")
    clock = pygame.time.Clock()

    player = Player()
    ground_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)

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
        player.update(keys)

        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (50, 205, 50), ground_rect)
        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
