import pygame
import random

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hangman")

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 40

# Load images and fonts
hangman_images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]
font = pygame.font.SysFont('arial', FONT_SIZE)

# Word list
word_list = ["PYTHON", "DEVELOPER", "PROGRAMMING", "HANGMAN", "PYGAME", "COMPUTER", "SCIENCE", "ALGORITHM", "FUNCTION", "VARIABLE"]
word = random.choice(word_list).upper()

# Game variables
hangman_status = 0
guessed = []

# Function to draw game elements
def draw():
    window.fill(WHITE)
    
    # Draw word with guessed letters
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = font.render(display_word, True, BLACK)
    window.blit(text, (400, 200))
    
    # Draw hangman image
    window.blit(hangman_images[hangman_status], (150, 100))
    pygame.display.update()

# Function to handle user input
def handle_input():
    global hangman_status
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if pygame.K_a <= event.key <= pygame.K_z:
                guessed_letter = chr(event.key).upper()
                if guessed_letter not in guessed:
                    guessed.append(guessed_letter)
                    if guessed_letter not in word:
                        hangman_status += 1

# Main game loop
run = True
while run:
    draw()
    handle_input()
    
    # Check for win/loss conditions
    if set(word).issubset(set(guessed)):
        print("You won!")
        run = False
    if hangman_status == 6:
        print("You lost! The word was:", word)
        run = False
    
    pygame.time.delay(100)

# Optionally, function to reset the game
def reset_game():
    global hangman_status, guessed, word
    hangman_status = 0
    guessed = []
    word = random.choice(word_list).upper()
