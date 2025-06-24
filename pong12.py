
# pong12
# Code With Mr Wagner
# your name

import pygame, time, random
from pygame.locals import *

pygame.init()

#variables
ScreenWidth = 800
ScreenHeight = 600

BallX = random.randint(300,500)
BallY = random.randint(100,500)
BallLocation = (BallX, BallY) #tuple
BallSize = 10
BallHalf = BallSize / 2 
dx = 3 #change in x
dy = 3

RPaddleX = 700
RPaddleY = 100
RPaddleW = 20
RPaddleH = 80
RPaddle = (RPaddleX, RPaddleY, RPaddleW, RPaddleH)
RPaddleUpOrDown = 0

LPaddleX = 100
LPaddleY = 100
LPaddleW = 20
LPaddleH = 80
LPaddle = (LPaddleX, LPaddleY, LPaddleW, LPaddleH)

# tuple (x,y,y,q)
# Constant
#       (red, green, blue) 0 and 255
WHITE = (255,255,255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# create a window
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode( (ScreenWidth,ScreenHeight) )
MyFont = pygame.font.SysFont(None, 100)

CenterOfScreen = ScreenWidth / 2
NetWidth = 10
LeftSideOfNet = CenterOfScreen - (NetWidth / 2)

# standard pygame game loop  while, for, if
GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                print("Down Key")
                RPaddleUpOrDown = 3
            if event.key == K_UP:
                print("Up Key")
                RPaddleUpOrDown = -3
        if event.type == KEYUP:
            if event.key == K_DOWN or event.key == K_UP:
                RPaddleUpOrDown = 0

                

    # == MEANS IS EQUAL TO  IF X == 10 RETURN TRUE OR FALSE
    # = MEANS ASSIGNED TO  X=10   
                

    BallX += dx
    BallY += dy
    BallLocation = (BallX, BallY) #tuple

    #bounce code
    if BallX > ScreenWidth - BallHalf or BallX < BallHalf:
        dx *= -1
    if BallY > ScreenHeight - BallHalf or BallY < BallHalf:
        dy *= -1

    #Collision detection w/ RPaddle
    if BallX + BallHalf > RPaddleX and \
       BallY > RPaddleY and \
       BallY < RPaddleY + RPaddleH:
        dx *= -1

    #Collision detection w/ LPaddle
    if BallX - BallHalf < LPaddleX + LPaddleW and \
       BallY > LPaddleY and \
       BallY < LPaddleY + LPaddleH:
        dx *= -1

    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, (LeftSideOfNet,0,NetWidth,ScreenHeight))
    pygame.draw.circle(screen, RED, BallLocation, BallSize, BallSize)

    RPaddleY += RPaddleUpOrDown
    RPaddle = (RPaddleX, RPaddleY, RPaddleW, RPaddleH)
    pygame.draw.rect(screen, BLUE, RPaddle)


    if BallY > LPaddleY + LPaddleH /2: #below bottom half of left paddle
        LPaddleY += random.randint(-1,5)
    else: #above
        LPaddleY -= random.randint(-1,5)

    LPaddle = (LPaddleX, LPaddleY, LPaddleW, LPaddleH)
    pygame.draw.rect(screen, GREEN, LPaddle)

    TextImg = MyFont.render('00', True, BLUE, WHITE)
    screen.blit(TextImg, (430,10))

    TextImg = MyFont.render('00', True, GREEN, WHITE)
    screen.blit(TextImg, (290,10))

    pygame.display.update()
    time.sleep(0.001)
# end of the while loop

print("Game Over")
pygame.quit()
