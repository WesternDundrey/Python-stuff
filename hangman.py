import pygame
import random

word_list = ["PYTHON", "DEVELOPER", "PROGRAMMING", "HANGMAN", "PYGAME", "COMPUTER", "SCIENCE", "ALGORITHM", "FUNCTION", "VARIABLE"]
pygame.init()
window = pygame.display.set_mode(width=800, height=600)
pygame.display.set_caption("Hangman")

white = (255,255,255)
black = (0,0,0)
font_size = 40

hangman_images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]
font = pygame.front.Sysfont('arial', font_size)

hangman_status = 0
print(hangman_status)
guessed = []
word = random.choice(word_list).upper()


def draw():
    window.fill(white)
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + ""
        else:
            display_word +="_ "
    text = font.render(display_word,True, black)
    window.blit(text,(400,200))
    window.blit(hangman_images,[hangman_status], (150,100))
    pygame.display.update()

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                guessed_letter = chr(event.key)
                if guessed_letter not in guessed:
                    guessed.append(guessed_letter)
                    if guessed_letter not in word:
                        global hangman_status
                        hangman_status += 1
run = True
while run:
    draw()
    handle_input()
    if set(word).issubset(set(guessed)):
        print("you won!")
        run = False
    if hangman_status == 6:
        print("You lost! The word was:", word)
        run = False
    pygame.time.delay(100)
