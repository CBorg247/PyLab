import pygame
import time

#inicio del juego
pygame.init()
#pantalla

display_width = 800
display_height = 600

#Colores en la pantalla
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
blue = (80, 160, 255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
#presentación 
pygame.display.set_caption("Haudi duin")
#tiempo: create an object to help track time/ Times in pygame are represented in milliseconds (1/1000 seconds)
clock = pygame.time.Clock()

Background = pygame.image.load("Background.png")
HeroImg = pygame.image.load("HaudiHero.png").convert_alpha()
HeroImg = pygame.transform.scale(HeroImg, (128, 128))  # 32×4
def Hero(x,y):
    gameDisplay.blit(HeroImg, (x,y))
def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText =pygame.font.SysFont("PressStart2P", 72)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash():
    message_display("Try again buddy")

def game_loop ():
    x = (display_width * 0.1)
    y = (display_height * 0.5)

    y_change = 0
    x_change = 0

    #Game loop (Se da algo hasta que no se da más por X razón)
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        x += x_change
        y += y_change

        # Actualiza la pantalla con el tiempo 
        
        gameDisplay.blit(Background, (0, 0))
        Hero(x,y)

        if x > display_width or x < 0:
            crash()
            gameExit = True
        elif y > display_height or y < 0:
            crash()
            gameExit = True

        pygame.display.update()
        clock.tick(60)   # 60 FPS

#Fin del juego
game_loop()
pygame.quit()
quit()