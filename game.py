import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple 2D Platformer')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Player settings
player_size = (50, 50)
player = pygame.Rect(100, 100, *player_size)
player_speed = 5
player_gravity = 0.5
player_jump_speed = -10
player_velocity_x = 0
player_velocity_y = 0
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, 550, 800, 50),   # Ground platform
    pygame.Rect(200, 400, 200, 20), # Floating platform
    pygame.Rect(500, 300, 200, 20)  # Floating platform
]

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Player horizontal movement
    if keys[pygame.K_LEFT]:
        player_velocity_x = -player_speed
    elif keys[pygame.K_RIGHT]:
        player_velocity_x = player_speed
    else:
        player_velocity_x = 0  # Stop horizontal movement if no key is pressed

    # Player jumping
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = player_jump_speed
        on_ground = False

    # Apply gravity
    player_velocity_y += player_gravity

    # Update player position
    player.x += player_velocity_x
    player.y += player_velocity_y

    # Check for collisions and update player position
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform):
            if player_velocity_y > 0 and player.bottom <= platform.bottom:
                player.bottom = platform.top
                player_velocity_y = 0
                on_ground = True
            elif player_velocity_y < 0 and player.top >= platform.top:
                player.top = platform.bottom
                player_velocity_y = 0

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, player)
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, platform)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
