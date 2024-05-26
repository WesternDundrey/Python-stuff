import pygame
pygame.init()
window = pygame.display.set_mode(width=800, height=600)
pygame.display.set_caption("Hangman")

white = (255,255,255)
black = (0,0,0)
font_size = 40

hangman_images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]
font = pygame.front.Sysfont('arial', font_size)

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

