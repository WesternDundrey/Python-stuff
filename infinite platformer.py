import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = BLUE

# Platform settings
PLATFORM_COLOR = WHITE
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
        self.change_y = 0
        self.jump_power = 10

    def update(self):
        self.rect.y += self.change_y
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.change_y = 0

    def jump(self):
        self.change_y = -self.jump_power

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def create_platforms(level):
    platforms = pygame.sprite.Group()
    num_platforms = random.randint(5, 10)
    for _ in range(num_platforms):
        width = random.randint(50, 150)
        height = PLATFORM_HEIGHT
        x = random.randint(0, SCREEN_WIDTH - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        platform = Platform(x, y, width, height)
        platforms.add(platform)
    return platforms

def main():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Platformer Game")

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    level = 1
    platforms = create_platforms(level)
    all_sprites.add(platforms)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        all_sprites.update()

        # Check if player reaches the bottom of the screen
        if player.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            level += 1
            player.jump_power += 1
            platforms = create_platforms(level)
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)
            all_sprites.add(platforms)
            player.rect.y = 0

        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
