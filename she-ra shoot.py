import pygame

#inicio del juego
pygame.init()
#pantalla

display_width = 800
display_height = 600

#Colores en la pantalla
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
#presentación 
pygame.display.set_caption("Haudi duin")
#tiempo: create an object to help track time/ Times in pygame are represented in milliseconds (1/1000 seconds)
clock = pygame.time.Clock()


HeroImg = pygame.image.load("HaudiHero.png")
def Hero(x,y):
    gameDisplay.blit(HeroImg, (x,y))

x = 
y =

#Game loop (Se da algo hasta que no se da más por X razón)
Died = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Died = True
    
    # Actualiza la pantalla con el tiempo 
    
    pygame.display.update()
    clock.tick(60)   # 60 FPS

#Fin del juego
pygame.quit()
quit()