
# pong6
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
BallSize = 10
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

CenterOfScreen = ScreenWidth / 2
NetWidth = 10
LeftSideOfNet = CenterOfScreen - (NetWidth / 2)

# standard pygame game loop  while, for, if
GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False

    BallX += dx
    BallY += dy
    BallLocation = (BallX, BallY) #tuple

    #bounce code
    if BallX > ScreenWidth - BallSize/2 or BallX < BallSize/2:
        dx *= -1
    if BallY > ScreenHeight - BallSize/2 or BallY < BallSize/2:
        dy *= -1

    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (LeftSideOfNet,0,NetWidth,ScreenHeight))
    pygame.draw.circle(screen, RED, BallLocation, BallSize, BallSize)

    pygame.display.update()
    time.sleep(0.001)
# end of the while loop

print("Game Over")
pygame.quit()
