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
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        # Find the leftmost platform
        leftmost_platform = min(platforms, key=lambda p: p.rect.x)
        self.rect.x = leftmost_platform.rect.x + (leftmost_platform.rect.width - PLAYER_WIDTH) // 2
        self.rect.y = leftmost_platform.rect.y - PLAYER_HEIGHT
        self.change_y = 0
        self.change_x = 0
        self.jump_power = 10
        self.gravity = 0.5

    def update(self):
        self.calc_gravity()
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Prevent moving out of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Check if player hits the bottom of the screen
        if self.rect.top >= SCREEN_HEIGHT:
            return True  # Indicate game over
        return False
    
    def calc_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += self.gravity

    def jump(self):
        self.change_y = -self.jump_power

    def move_left(self):
        self.change_x = -5

    def move_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0


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
    num_platforms = 4  # Always create 4 platforms
    for _ in range(num_platforms):
        width = random.randint(50, 150)
        height = PLATFORM_HEIGHT
        x = random.randint(0, SCREEN_WIDTH - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        platform = Platform(x, y, width, height)
        platforms.add(platform)
    return platforms
#yababababa
def main():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption("Platformer Game")

    def reset_game():
        nonlocal level, platforms, player, all_sprites, pole
        level = 1
        platforms = create_platforms(level)
        player = Player(platforms)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        all_sprites.add(platforms)
        pole = Pole(SCREEN_WIDTH - POLE_WIDTH, SCREEN_HEIGHT - POLE_HEIGHT - PLATFORM_HEIGHT, POLE_WIDTH, POLE_HEIGHT)
        all_sprites.add(pole)

    reset_game()
    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = False
                        reset_game()
                    if event.key == pygame.K_q:
                        running = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    if event.key == pygame.K_RIGHT:
                        player.move_right()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_RIGHT and player.change_x > 0:
                        player.stop()

        if not game_over:
            all_sprites.update()

            # Check if player hits the bottom of the screen
            if player.update():
                game_over = True

            # Check for collision with platforms
            if pygame.sprite.spritecollide(player, platforms, False):
                player.change_y = 0
                player.rect.y = min([p.rect.top for p in platforms if player.rect.colliderect(p.rect)]) - PLAYER_HEIGHT

            # Check if player reaches the right edge of the screen or the pole
            if player.rect.right >= SCREEN_WIDTH or pygame.sprite.collide_rect(player, pole):
                level += 1
                player.jump_power += 1
                platforms = create_platforms(level)
                player = Player(platforms)
                all_sprites = pygame.sprite.Group()
                all_sprites.add(player)
                all_sprites.add(platforms)
                pole = Pole(SCREEN_WIDTH - POLE_WIDTH, SCREEN_HEIGHT - POLE_HEIGHT - PLATFORM_HEIGHT, POLE_WIDTH, POLE_HEIGHT)
                all_sprites.add(pole)

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)

        if game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, RED)
            screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

            font = pygame.font.Font(None, 36)
            text = font.render("Press R to Replay or Q to Quit", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

