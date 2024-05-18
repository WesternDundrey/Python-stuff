import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simple 2D Platformer')

# Colors
BACKGROUND_COLOR = (30, 30, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (70, 130, 180)
PLATFORM_COLOR = (169, 169, 169)
DEADLY_PLATFORM_COLOR = (220, 20, 60)
BUTTON_COLOR = (34, 139, 34)
BUTTON_HOVER_COLOR = (50, 205, 50)
TEXT_COLOR = (255, 255, 255)

# Player settings
player_size = (50, 50)
player_start_pos = (100, 100)
player = pygame.Rect(*player_start_pos, *player_size)
player_speed = 5
player_gravity = 0.5
player_jump_speed = -15  # Increase jump height
player_velocity_x = 0
player_velocity_y = 0
on_ground = False
dead = False
game_started = False

# Platforms
platforms = [
    pygame.Rect(0, 550, 800, 50),   # Ground platform
    pygame.Rect(150, 450, 200, 20), # Left safe platform
    pygame.Rect(400, 450, 200, 20), # Deadly platform in the middle
    pygame.Rect(650, 450, 200, 20), # Right safe platform
    pygame.Rect(475, 350, 50, 20)   # Small platform above the deadly platform
]

# Main game loop
running = True
clock = pygame.time.Clock()

def reset_game():
    global player, player_velocity_x, player_velocity_y, on_ground, dead, game_started
    player = pygame.Rect(*player_start_pos, *player_size)
    player_velocity_x = 0
    player_velocity_y = 0
    on_ground = False
    dead = False
    game_started = False

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for mouse click events on the death screen
        if dead and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if replay_button.collidepoint(mouse_pos):
                reset_game()
            elif exit_button.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    if not dead:
        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Start the game on first move
        if not game_started and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            game_started = True

        if game_started:
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
                    if platform == platforms[2]:  # Deadly platform
                        dead = True
                        break
                    if player_velocity_y > 0 and player.bottom <= platform.bottom:
                        player.bottom = platform.top
                        player_velocity_y = 0
                        on_ground = True
                    elif player_velocity_y < 0 and player.top >= platform.top:
                        player.top = platform.bottom
                        player_velocity_y = 0

    # Draw everything
    screen.fill(BACKGROUND_COLOR)

    if dead:
        # Display "You Died" message
        font = pygame.font.SysFont(None, 55)
        text = font.render("You Died", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 - 50))

        # Render "Replay" button
        replay_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, replay_button, border_radius=10)
        replay_text = font.render("Replay", True, BLACK)
        screen.blit(replay_text, (replay_button.x + replay_button.width // 2 - replay_text.get_width() // 2, replay_button.y + replay_text.get_height() // 2))

        # Render "Exit" button
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, exit_button, border_radius=10)
        exit_text = font.render("Exit", True, BLACK)
        screen.blit(exit_text, (exit_button.x + exit_button.width // 2 - exit_text.get_width() // 2, exit_button.y + exit_text.get_height() // 2))
    else:
        # Draw player as a circle
        pygame.draw.ellipse(screen, PLAYER_COLOR, player)

        # Draw platforms
        for i, platform in enumerate(platforms):
            if platform == platforms[2]:  # Deadly platform
                draw_rounded_rect(screen, DEADLY_PLATFORM_COLOR, platform, 10)
            else:
                draw_rounded_rect(screen, PLATFORM_COLOR, platform, 10)

        # Display start text if the game hasn't started yet
        if not game_started:
            font = pygame.font.SysFont(None, 40)
            start_text = font.render("Press LEFT or RIGHT arrow key to start", True, TEXT_COLOR)
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - start_text.get_height() // 2 - 150))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
