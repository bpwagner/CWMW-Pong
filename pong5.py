
# pong2
# Code With Mr Wagner
# your name

import pygame, time
pygame.init()

#variables
ScreenWidth = 800
ScreenHeight = 600

BallX = 100
BallY = 100
BallLocation = (BallX, BallY) #tuple
dx = 1 #change in x
dy = 1 


# tuple (x,y,y,q)
# Constant
#       (red, green, blue) 0 and 255
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


# create a window
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode( (ScreenWidth,ScreenHeight) )

# standard pygame game loop  while, for, if
GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False

    # newValue = oldValue +1
    BallX = BallX + dx
    BallY = BallY + dy
    BallLocation = (BallX, BallY) #tuple

    if BallY > 600 or BallY < 0:
        dy = dy * -1
    #if BallY < 0:
    #    dy = dy * -1

    if BallX > 800 or BallX < 0:
        dx = dx * -1
    #if BallX < 0:
    #    dx = dx * -1
            

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, BallLocation, 10, 5)
    pygame.draw.rect(screen, BLACK, (395,0,10,600))

    pygame.display.update()
    time.sleep(0.001)
# end of the while loop
print("Game Over")
pygame.quit()
