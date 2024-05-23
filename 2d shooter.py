import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Shooter")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the player
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 20
player_speed = 5

# Set up the bullet
bullet_width = 5
bullet_height = 15
bullet_speed = 10
bullet_color = (255, 0, 0)
bullets = []

# Set up the enemies
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

def create_enemy():
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = random.randint(-500, -enemy_height)
    enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

# Create initial row of enemies at the top
for i in range(10):
    create_enemy()

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + (player_width - bullet_width) // 2
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
    
    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    
    # Move bullets
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)
    
    # Move enemies
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > screen_height:
            enemies.remove(enemy)
            create_enemy()
    
    # Check for collisions between bullets and enemies
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                create_enemy()
    
    # Draw player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, bullet_color, bullet)
    
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    
    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
