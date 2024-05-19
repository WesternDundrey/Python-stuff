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
RED = (255, 0, 0)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = BLUE

# Platform settings
PLATFORM_COLOR = WHITE
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

# Pole settings
POLE_WIDTH = 10
POLE_HEIGHT = 100
POLE_COLOR = RED

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - PLATFORM_HEIGHT
        self.change_y = 0
        self.jump_power = 10
        self.gravity = 0.5

    def update(self):
        self.calc_gravity()
        self.rect.y += self.change_y
        
        # Check if player is on the ground
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.change_y = 0

    def calc_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += self.gravity

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

class Pole(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def create_platforms(level):
    platforms = pygame.sprite.Group()
    num_platforms = random.randint(1, 4)
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
    
    pole = Pole(SCREEN_WIDTH - POLE_WIDTH, SCREEN_HEIGHT - POLE_HEIGHT - PLATFORM_HEIGHT, POLE_WIDTH, POLE_HEIGHT)
    all_sprites.add(pole)
    
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

        # Check for collision with platforms
        if pygame.sprite.spritecollide(player, platforms, False):
            player.change_y = 0
            player.rect.y = min([p.rect.top for p in platforms if player.rect.colliderect(p.rect)]) - PLAYER_HEIGHT

        # Check if player reaches the right edge of the screen or the pole
        if player.rect.right >= SCREEN_WIDTH or pygame.sprite.collide_rect(player, pole):
            level += 1
            player.jump_power += 1
            platforms = create_platforms(level)
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)
            all_sprites.add(platforms)
            pole = Pole(SCREEN_WIDTH - POLE_WIDTH, SCREEN_HEIGHT - POLE_HEIGHT - PLATFORM_HEIGHT, POLE_WIDTH, POLE_HEIGHT)
            all_sprites.add(pole)
            player.rect.x = 0  # Reset player's position to the start
            player.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - PLATFORM_HEIGHT

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
           
