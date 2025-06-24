
# pong4
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
    BallX = BallX + 1
    BallY = BallY + 1
    BallLocation = (BallX, BallY) #tuple
            

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, BallLocation, 10, 5)
    pygame.draw.rect(screen, BLACK, (395,0,10,600))

    pygame.display.update()
    time.sleep(0.01)
# end of the while loop
print("Game Over")
pygame.quit()
