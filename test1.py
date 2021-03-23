#pygame trex
import pygame
from pygame.locals import *
#modules initialized
pygame.init()
#screen size
scr = pygame.display.set_mode((600,500))
pygame.display.set_caption("Trex try1")
#font
font = pygame.font.Font("freesansbold.ttf", 20)
#images
background = pygame.image.load("trex_pics/background.png")
dragon = pygame.image.load("trex_pics/dra1.png")
dragon = pygame.transform.scale(dragon, (50,50))
dragon2 = pygame.image.load("trex_pics/dra2.png")
dragon2 = pygame.transform.scale(dragon2, (50,50))
dragon3 = pygame.image.load("trex_pics/dra3.png")
dragon3 = pygame.transform.scale(dragon3, (50,50))
dragon4 = pygame.image.load("trex_pics/dra4.png")
dragon4 = pygame.transform.scale(dragon4, (50,50))
dragon5 = pygame.image.load("trex_pics/dra6.png")
dragon5 = pygame.transform.scale(dragon5, (50,50))
walk = [dragon, dragon, dragon, dragon, dragon2, dragon2, dragon2, dragon2, dragon3, dragon3, dragon3, dragon3, dragon4, dragon4, dragon4, dragon4]
tree = pygame.image.load("trex_pics/tree.png")
tree = pygame.transform.scale(tree, (70, 50))
tree1 = pygame.image.load("trex_pics/tree1.png")
tree1 = pygame.transform.scale(tree1, (100, 60))
tree2 = pygame.image.load("trex_pics/tree2.png")
tree2 = pygame.transform.scale(tree2, (90, 60))
tree3 = pygame.image.load("trex_pics/tree3.png")
tree3 = pygame.transform.scale(tree3, (45, 60))
tree4 = pygame.image.load("trex_pics/tree4.png")
tree4 = pygame.transform.scale(tree4, (70, 60))

def gameloop():
    #variables
    backx = 0
    backy = 0
    backvelo = 0
    treex = 550
    treey = 282
    #treevelo = 0
    dragx = 50
    dragy = 275
    walkpoint = 0
    game = False
    jump = False
    gravity = 7
    score = 0
    gameover = False
    while True:
         #colours
        white = (255, 255, 255)
        black = (0, 0, 0)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if dragy == 275:
                        jump = True
                        backvelo = 6
                        game = True
                if event.key == K_SPACE:
                    if gameover == True:
                        gameloop()

        if backx == -600:
            backx = 0
        if treex < -1600:
            treex = 550
        #jump
        if 276 > dragy > 125:
            if jump == True:
                dragy -= 7
        else:
            jump = False
        if dragy < 275:
            if jump == False:
                dragy += gravity

        #collision
        if treex < dragx + 50 < treex + 70 and treey < dragy + 50 < treey + 50:
            backvelo = 0            
            walkpoint = 0
            game = False
            gameover = True
        if treex + 400 < dragx + 50 < treex + 470 and treey < dragy + 50 < treey + 50:
            backvelo = 0            
            walkpoint = 0
            game = False
            gameover = True
        if treex + 800 < dragx + 50 < treex + 870 and treey < dragy + 50 < treey + 50:
            backvelo = 0            
            walkpoint = 0
            game = False
            gameover = True
        if treex + 1200 < dragx + 50 < treex + 1270 and treey < dragy + 50 < treey + 50:
            backvelo = 0            
            walkpoint = 0
            game = False
            gameover = True
        if game == True:
            score += 1


        scr.fill(white)
        text = font.render("Score: " + str(score), True, black)
        text1 = font.render("Game over! Press Space to continue ", True, black)
        backx -= backvelo
        treex -= backvelo

        scr.blit(background, [backx, backy])
        scr.blit(background, [backx+600, backy])
        scr.blit(text, [400, 150])
        if gameover == True:
            scr.blit(text1, [50, 350])
         #walking legs
        scr.blit(walk[walkpoint], [dragx, dragy])
        if game == True:
            walkpoint += 1
            if walkpoint > 15:
                walkpoint = 0
        scr.blit(tree, [treex, treey])
        scr.blit(tree1, [treex + 400, treey])
        scr.blit(tree2, [treex + 800, treey])
        scr.blit(tree3, [treex + 1200, treey])
        scr.blit(tree4, [treex + 1600, treey])
        pygame.display.update()  

gameloop()    
    