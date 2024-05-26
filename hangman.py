import pygame
pygame.init()
window = pygame.display.set_mode(width=800, height=600)
pygame.display.set_caption("Hangman")

white = (255,255,255)
black = (0,0,0)
font_size = 40

hangman_images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]
font = pygame.front.Sysfont('arial', font_size)
guessed = input("Guess a letter!")
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
