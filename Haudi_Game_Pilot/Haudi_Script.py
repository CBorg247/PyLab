import pygame
import time
import random

pygame.init()
#crash_sound = pygame.mixer.Sound("")-En el proximo le pongo musica TODO
#pygame.mixer.music.load("")TODO 

display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
blue = (80, 160, 200)
brown = (139,69,19)
light_brown = (160,82,45)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("HaudiDuin")
clock = pygame.time.Clock()

#Carga de imagenes
Background = pygame.image.load("Background.png")
HeroImg = pygame.image.load("HaudiHero.png").convert_alpha()
HeroImg = pygame.transform.scale(HeroImg, (128, 128))  # 32×4
Bullet = pygame.image.load("Fireball.png")
Bullet = pygame.transform.scale(Bullet, (128, 32))  # 32×4
Ranas = pygame.image.load("HaudiVillain2.png")
Ranas = pygame.transform.scale(Ranas, (512, 128))  # 32×4
Haudi_intro = pygame.image.load("Haudi_intro.png")
Screen_pause = pygame.image.load("screen_pause.png")
#Dead_Villain = pygame.image.load()
#Dead_Villain = pygame.transform.scale()
#Dead_HeroImg = pygame.image.load()
#Dead_HeroImg = pyame.transform.scale()
pygame.display.set_icon(HeroImg)
# TODO SPRITE DEADS

pause = False

def preparar_frames(sheet, frame_w, frame_h):
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        for i in range(0, sheet_width, frame_w):
            rect = pygame.Rect(i,0, frame_w, frame_h)
            frame = sheet.subsurface(rect)
            frames.append(frame) 
        return frames

Hero_frame = preparar_frames(HeroImg, 32, 32)
Villain_frame = preparar_frames(Ranas, 128, 128)
Bullet_frame = preparar_frames(Bullet, 32, 32)

def ranas(x, y, frame):
    gameDisplay.blit(Villain_frame[frame],(x,y))

def ranas_capturadas(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Ranas capturadas:" +str(count), True, black)
    gameDisplay.blit(text, (0,0))
    
def Hero(x,y):
    gameDisplay.blit(HeroImg, (x,y))

def Balas(balasx,balasy):
    gameDisplay.blit(Bullet, (balasx,balasy))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText =pygame.font.SysFont(None, 72)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)
    game_intro()

def game_over():
    
    #pygame.mixer.music.stop()
    #pygame.mixer.Sound.play(gameover_sound)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(black) #negro si pierdo
        largeText =pygame.font.SysFont(None, 72)
        TextSurf, TextRect = text_objects("Game Over", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        buttons("Reintenta",150,450, 100, 50,brown,light_brown, game_loop)
        buttons("Salir",550,450, 100, 50,brown,light_brown, "quit")

        pygame.display.update()
        clock.tick(15) 

def buttons(msg,x,y,w,h,ic,ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y, w, h))
        if click[0] == 1 and action !=None:
            if action =="play": #Ver funciones acá
                game_loop()
            elif action =="quit": #punteros a funciones
                pygame.quit()
                quit()
            elif action != None:
                action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x,y, w, h))
    smalltext = pygame.font.Font(None, 20)
    textSurf, TextRect = text_objects (msg, smalltext)
    TextRect.center = ((x +(w/2), (y + (h/2))))
    gameDisplay.blit(textSurf, TextRect)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(Haudi_intro,(0,0)) #acá es donde pongo el dibujo 

        buttons("Jugar",150,450, 100, 50,brown,light_brown, "play")
        buttons("Salir",550,450, 100, 50,brown,light_brown, "quit")

        pygame.display.update()
        clock.tick(15) 

def unpause():
    global pause
    #pygame.mixer.music.unpause()
    pause = False
    
def paused():
    
    #pygame.mixer.music.pause()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
        gameDisplay.blit(Screen_pause,(0,0))

        buttons("Continuar",150,450, 100, 50,brown,light_brown, unpause)
        buttons("Salir",550,450, 100, 50,brown,light_brown, "quit")

        pygame.display.update()
        clock.tick(15) 

def game_loop ():
    global pause
    #pygame.mixer.music.play(-1)
    x = (display_width * 0.1)
    y = (display_height * 0.5)

    y_change = 0
    x_change = 0

    ranas_starty = random.randrange(0, display_height)
    ranas_startx = display_width + 100
    ranas_speed = 3
    ranas_width = 100
    ranas_height = 100
    bullets = []
    score = 0

    def respawn_ranas():
         return display_width + 200, random.randrange(0, display_height - 100)

    #Game loop
    gameExit = False
    max_bullets = 20
    bullets_fired = 0
    villain_frame_index = 0
    hero_frame_index = 0
    bullet_frame_index = 0

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                elif event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_p:
                    pause = True
                    paused()

                if event.key == pygame.K_SPACE and bullets_fired < max_bullets:
                    bullets.append([x+60, y+60])
                    bullets_fired += 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

            villain_frame_index += 0.7
            if villain_frame_index >= len(Villain_frame):
                villain_frame_index = 0
                
        x += x_change
        y += y_change

        # Actualización de pantalla 
        gameDisplay.blit(Background, (0, 0))
        ranas(ranas_startx, ranas_starty, int(villain_frame_index))
        ranas_startx -= ranas_speed
        Hero(x,y)
        player_rect = pygame.Rect(x, y, 128, 128)
        rana_rect = pygame.Rect(ranas_startx, ranas_starty, ranas_width, ranas_height)

        #COLISIONES
        for bullet in bullets[:]:
            bullet[0] += 10
            Balas(bullet[0], bullet[1])

            bullet_rect = pygame.Rect(bullet[0], bullet[1], 128, 32)

            if bullet_rect.colliderect(rana_rect):
                score += 1
                bullets.remove(bullet)
                ranas_startx, ranas_starty = respawn_ranas()

            if bullet[0] > display_width:
                bullets.remove(bullet)
        #puntaje
        ranas_capturadas(score)
        if bullets_fired >= max_bullets and score < 20 and len(bullets) == 0:
            game_over()
        
        if x < 0 or x > display_width-128 or y < 0 or y > display_height-128:
            game_over()
            gameExit = True
        
        if ranas_startx < -ranas_width:
            ranas_startx, ranas_starty = respawn_ranas()
            ranas_speed += 1

        if player_rect.colliderect(rana_rect):
            game_over()

        if score >= 20:
            message_display("¡Misión completa!")

        pygame.display.update()
        clock.tick(60)   # 60 FPS

#Fin del juego
game_intro()
game_loop()
pygame.quit()
quit()