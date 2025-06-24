# Pong

import pygame, time, math, random
from pygame.locals import *


#Handicap Options
#ChangeBall will give a larger ball to the player who is behind
ChangeBall = False
#ChangePaddle will give a smaller paddle to the player who is ahead
ChangePaddle = False
#ChangeSpeed will speed up th ball to the player who is ahead
ChangeSpeed = False

#CONSTANTS
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,180)
GREEN = (0,180,0)
PIHALF = math.pi/2
#We want to limit the angles for the ball's vector so that they don't become too vertical or flip directions.
#Due to the mapping of the screen space not matching normal Cartesian plane
#So a 45degree angle would be due NE in Cartesian, but SE in this configuration.
#And a 135degree angle would be NW in Cartesian, but is SW in this space.
#Need to remember this planar reflection as I play with angles

pygame.init()

MaxScore = 21
LScore=0
RScore=0

ScreenWidth = 800
ScreenHeight = 600
FontSize = int(ScreenHeight/10)
ScoreY = ScreenHeight/60 # Horizontal placement of score text
ScoreLX = ScreenWidth/2 - (FontSize) #Yes, I know the font size is not the width, but this should still give some scale
ScoreRX = ScreenWidth/2 + ScreenWidth/80

StartBallRadius = 10 #Default Ball Size
BallRadius = 0 #Size of Ball on the screen. Intially 0 so that it does not appear on the screen while waiting to start (radius = 0)
LBallRadius = BallRadius #Used if the ChangeBall handicap is enabled
RBallRadius = BallRadius
BallX = ScreenWidth/2
BallY = ScreenHeight/2
StartBallSpeed = 3 #Default Ball Speed
BallSpeed = 0 #Current speed of Ball on the screen.  Initially 0 since we are not playing yet
LBallSpeed = StartBallSpeed #Used ifthe ChangeSpeed handicap is enabled
RBallSpeed = StartBallSpeed

NetW = ScreenWidth/200 #Width of the Net
NetL = ScreenWidth/2-NetW/2
ScreenBottomCheck = ScreenHeight-StartBallRadius-1 #Similarly, subtract 1 from the Height

PaddleGap = 10 # Gap between edge of screen and closest edge of paddle
PaddleSpeed = 3 # Maybe make this dynamic based upon BallSpeed
StartPaddleH = int(ScreenHeight/10)
PaddleW = int(ScreenWidth/40)
RPaddleH = StartPaddleH
RPaddleHHalf = RPaddleH>>1 #Kept using half the paddle height in calculations.  May as well make it a variable
RPaddleX = int(ScreenWidth-(PaddleW+PaddleGap))
RPaddleY = ScreenHeight/2-RPaddleHHalf
RPaddleLimit = ScreenHeight-RPaddleH #Used to prevent paddle scrolling off screen
RPaddleMove = 0
RPaddle = (RPaddleX, RPaddleY, PaddleW, RPaddleH)
RPast = False #Used to see if ball got past paddle before it had a chance to hit it (possible for high speed balls).  Give person one chance to have the paddle in the right spot before declaring the ball got past them.
LPaddleH = StartPaddleH
LPaddleHHalf = LPaddleH>>1
LPaddleX = PaddleGap
LPaddleEdgeX = PaddleW+PaddleGap #Right side of the left paddle - used to detect ball collision detection
LPaddleY = ScreenHeight/2-LPaddleHHalf
LPaddleLimit = ScreenHeight-LPaddleH
#LPaddleMove = 0
LPaddle = (LPaddleX, LPaddleY, PaddleW, LPaddleH)
LPast = False

MinStartAngle = 15/180*math.pi #Start angle is random, but needs to be scoped
MaxStartAngle = 75/180*math.pi
MaxAngSW = 100/180*math.pi
MaxAngSE = 80/180*math.pi
MaxAngNE = -MaxAngSE
MaxAngNW = -MaxAngSW
dAngMax = math.pi/18 #Max angle change off a paddle will be 10 degrees

# Ball angle is in MinStartAngle to MaxStartAngle rotated randomly by 90 or 180 degrees
BallAngle = random.uniform(MinStartAngle, MaxStartAngle)*random.choice([-1,1])+math.pi*random.choice([-1,0])
Left2Right = (BallAngle > -math.pi/2) and (BallAngle < math.pi/2) #Direction of ball

#create a window
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))
MyFont = pygame.font.SysFont(None, FontSize)
MyFont2 = pygame.font.SysFont(None, FontSize>>1)
#DebugFont = pygame.font.SysFont(None, 20)
#TextDImg = DebugFont.render("",True,BLUE, WHITE)


# Main game loop
GameRunning = True
while GameRunning:
    #Using vectors for ball movement.  BallSpeed is the magnitude and BallAngle is th angle
    dx = BallSpeed*math.cos(BallAngle)
    dy = BallSpeed*math.sin(BallAngle)
    BallLocation = (BallX, BallY)

    for event in pygame.event.get():
        if event.type == QUIT:
            GameRunning = False
        elif event.type == KEYDOWN:
            if event.key == K_DOWN:
                RPaddleMove = PaddleSpeed
            if event.key == K_UP:
                RPaddleMove = -PaddleSpeed
        elif event.type == KEYUP and (event.key == K_DOWN or event.key == K_UP):
            RPaddleMove = 0
        elif event.type == KEYUP and (event.key == K_SPACE) and dx==0: #time to start a new game and set up game variables
            RPast = False
            LPast = False
            Left2Right = True
            if (LScore == MaxScore) or (RScore == MaxScore): #Reset Scores if we have a winner
                LScore = 0
                RScore = 0
            BallAngle = random.uniform(MinStartAngle, MaxStartAngle)*random.choice([-1,1])
            dScore = LScore - RScore
            if dScore < 0:
                BallAngle += math.pi #Turn the ball around to the left player (player with lowest score hits first)
                Left2Right = False
            BallRadius = StartBallRadius
            BallSpeed=StartBallSpeed
            dx = BallSpeed*math.cos(BallAngle)
            dy = BallSpeed*math.sin(BallAngle)
            BallX = ScreenWidth/2 - dScore/MaxScore*ScreenWidth/4 #Adjust start of ball to give loser more time to react
            BallY = ScreenHeight/2
            TextMsg = MyFont2.render("",True,RED,WHITE)
            if ChangePaddle: #Adjust size of paddles of leader and loser
                if dScore == 0:
                    RPaddleH = StartPaddleH
                    RPaddleHHalf = RPaddleH>>1
                    LPaddleH = StartPaddleH
                    LPaddleHHalf = LPaddleH>>1
                elif dScore > 0: #Left is winning so make the right paddle bigger
                    if dScore > 10:
                        dScore = 10 #Cap the growth amount
                    RPaddleH = int((1+dScore*0.05)*StartPaddleH)
                    RPaddleHHalf = RPaddleH>>1
                    RPaddleLimit = ScreenHeight-RPaddleH
                    dScore = LScore - RScore - 10 # if over 10 ahead, then we start shrinking the left paddle
                    if dScore > 0:
                        if dScore > 10:
                            dScore = 10 #Cap the shrink amount
                        LPaddleH = int((1-dScore*0.07)*StartPaddleH)
                        LPaddleHHalf = LPaddleH>>1
                        LPaddleLimit = ScreenHeight-LPaddleH                    
                        LTop2 = LPaddleH * -0.05 
                        LTop1 = LPaddleH * -0.17 
                        LMed = LPaddleH * -0.83 
                        LBot1 = LPaddleH * -0.95 
                        LBot2 = -LPaddleH                                   
                else: #Right is winning
                    dScore *= -1
                    if dScore > 10:
                        dScore = 10 #Cap the growth amount
                    LPaddleH = int((1+dScore*0.05)*StartPaddleH)
                    LPaddleHHalf = LPaddleH>>1
                    LPaddleLimit = ScreenHeight-LPaddleH                    
                    LTop2 = LPaddleH * -0.05 
                    LTop1 = LPaddleH * -0.17 
                    LMed = LPaddleH * -0.83 
                    LBot1 = LPaddleH * -0.95 
                    LBot2 = -LPaddleH
                    dScore = RScore-LScore-10 
                    if dScore > 0: #start shrinking right paddle
                        if dScore > 10:
                            dScore = 10 #Cap the shrink amount
                        RPaddleH = int((1-dScore*0.07)*StartPaddleH)
                        RPaddleHHalf = RPaddleH>>1
                        RPaddleLimit = ScreenHeight-RPaddleH
                        RTop2 = RPaddleH * -0.05 
                        RTop1 = RPaddleH * -0.17 
                        RMed = RPaddleH * -0.83 
                        RBot1 = RPaddleH * -0.95 
                        RBot2 = -RPaddleH 
            if ChangeBall: #Adjust size of ball for leader and loser
                if dScore == 0:
                    RBallRadius = StartBallRadius
                    LBallRadius = StartBallRadius
                    BallRadius = StartBallRadius
                elif dScore > 0: #Left is winning so make the right ball bigger                
                    if dScore > 10:
                        dScore = 10
                    RBallRadius = (1+0.1*dScore)*StartBallRadius
                    dScore = LScore - RScore - 10
                    if dScore > 0: #Left winning by more than 10 so shrink the left ball
                        if dScore > 10:
                            dScore = 10
                        LBallRadius = (1-0.05*dScore)*StartBallRadius
                else: #Right is winning
                    dScore *= -1
                    if dScore > 10:
                        dScore = 10
                    LBallRadius = (1+0.1*dScore)*StartBallRadius
                    dScore = RScore - LScore - 10
                    if dScore > 0: #Right winning by more than 10 so shrink the left ball
                        if dScore > 10:
                            dScore = 10
                        RBallRadius = (1-0.05*dScore)*StartBallRadius
            if ChangeSpeed: #Adjust the speed of ball for leader and loser
                if dScore == 0:
                    RBallSpeed = StartBallSpeed
                    LBallSpeed = StartBallSpeed
                    BallSpeed = StartBallSpeed
                elif dScore > 0: #Left is winning so make the ball heading left go faster
                    if dScore > 10:
                        dScore = 10
                    LBallSpeed = (1+0.1*dScore)*StartBallSpeed
                    dScore = LScore-RScore-10
                    if dScore > 0: #Left winning by more than 10, slow down ball heading right
                        if dScore>10:
                            dScore = 10
                        RBallSpeed = (1-.05*dScore)*StartBallSpeed
                else:
                    dScore *= -1
                    if dScore > 10:
                        dScore = 10
                    RBallSpeed = (1+0.1*dScore)*StartBallSpeed
                    dScore = RScore-LScore-10
                    if dScore > 0: #Left winning by more than 10, slow down ball heading right
                        if dScore>10:
                            dScore = 10
                        LBallSpeed = (1-.05*dScore)*StartBallSpeed
                if Left2Right:
                    BallSpeed = RBallSpeed
                else:
                    BallSpeed = LBallSpeed
            
            
#Move Right/User Paddle and keep it on the screen
    RPaddleY += RPaddleMove
    if RPaddleY < 0:
        RPaddleY = 0
    if RPaddleY > RPaddleLimit:
        RPaddleY = RPaddleLimit
    RPaddle = (RPaddleX, RPaddleY, PaddleW, RPaddleH)
    
#Move Left/Computer Paddle and keep it on the screen
    if BallY<(LPaddleY+(LPaddleH>>1)):
        LPaddleY -= PaddleSpeed/2
        if LPaddleY < 0:
              LPaddleY = 0
    else:
        LPaddleY += PaddleSpeed/2
        if LPaddleY > LPaddleLimit:
            LPaddleY = LPaddleLimit
    if BallRadius > 0: #The wiggling of the paddle waiting for a game to start annoyed me.  This stops the paddle during that time
        LPaddle = (LPaddleX, LPaddleY, PaddleW, LPaddleH)


#This code block is just being fancy to grow/shrink the ball as it moves.
#If ChangeBall handicap is set then the ball will change size based upon the score delta and the direction of ball.
#I could have just reset the ball to the new size once it hit a paddle, but it was a bit jarring and sometimes caused the
#now larger ball to interfere with the paddle it had just hit.
    if ChangeBall and BallRadius > 0:
        BallChange = int(StartBallRadius*.1) #The increment of the ball change
        if BallChange == 0:
            BallChange = 1 
        if Left2Right: #Change ball to the size for the right player
            if BallRadius > RBallRadius: #We need to shrink
                BallRadius -= BallChange
            elif BallRadius < RBallRadius: #We need to grow
                BallRadius += BallChange
        else: #Change the ball to the size for the left player
            if BallRadius > LBallRadius:
                BallRadius -= BallChange
            elif BallRadius < LBallRadius:
                BallRadius += BallChange        
        ScreenBottomCheck = ScreenHeight-BallRadius-1 #readjust the bottom of screen check for the new radius
                
#Move ball to potentially new spot
    BallX += dx
    BallY += dy

#Right and left screen edge detection
    #Check if off the right edge and if it has already gone past the right paddle - safety net when ball speed may 'blast' through the paddle
    if BallX >= ScreenWidth and RPast:
        LScore += 1
        dx = 0 # This tells me a point has been won and the game is stopped and also stops the ball from moving

    #Check if off the left edge and has already gone past the left paddle
    if BallX < 0 and LPast:
        RScore += 1
        dx = 0
        
#Game is waiting for spacebar - Zero out some variables
    if dx==0:
        dy = 0
        BallSpeed=0
        BallRadius=0
        BallX = ScreenWidth/2
        BallY = ScreenHeight/2
        if LScore == MaxScore:
            TextMsg = MyFont2.render("Left Player Won!\nPress SPACE Bar To Start",True,GREEN,WHITE)
        elif RScore == MaxScore:
            TextMsg = MyFont2.render("Right Player Won!\nPress SPACE Bar To Start",True,BLUE,WHITE)
        else:
            TextMsg = MyFont2.render("Press SPACE Bar To Start",True,RED,WHITE)
            
#Top and bottom screen edge detection    
    if BallY >= ScreenBottomCheck or BallY <= BallRadius:
        BallAngle = -BallAngle #Keep track of change of direction, and this is always a true reflection
        if BallY < BallRadius:
            BallY = (BallRadius<<1) - BallY #Bring the ball back on the screen by the same amount it went off. Algebraicallly the same as BR-(BallY-BR), but multiply by 2 using a bit shift is very quick
        elif BallY > ScreenBottomCheck:
            BallY = (ScreenBottomCheck<<1) - BallY
        dx = BallSpeed*math.cos(BallAngle)
        dy = BallSpeed*math.sin(BallAngle)

#Right Paddle Edge Detection
    xDelta = RPaddleX-(BallX+BallRadius) #Gap between left edge of paddle and right edge of the ball
    yDelta = RPaddleY+RPaddleHHalf-BallY #Gap between middle of paddle and middle of the ball.  Note if - then ball is below center
    if not RPast and xDelta <= 0:
        RPast = True # This is the first time the ball got past or hit us.
                     # This 'saves' the ball if the speed is fast enough to go from the
                     # left side of the paddle to being past the paddle.
        LPast = False
        if abs(yDelta)<(RPaddleHHalf+BallRadius): # Check if we are within the paddle range +/- the ball radius (which could catch the paddle edges
            if (RPaddleX-BallX)<BallRadius:
                BallX = ((RPaddleX-BallRadius)<<1)-BallX #Similar to above where ball moved past the screen so now we keep it always left of the paddle
            # Calculate percentage of the hit length.  0 = Middle of paddle.  1 is top.  -1 is bottom.  Then points inbetween
            PadPercent = yDelta/(RPaddleHHalf+BallRadius)
            #Need to reflect the ball, so check if we are traveling NE or SE
            if BallAngle > 0:
                m1 = math.pi
            else:
                m1 = -math.pi
            BallAngle = m1-BallAngle+(dAngMax*PadPercent)
            #BallAngle needs to be bounded to MAXANGNW and MAXANGSW
            if BallAngle < 0 and BallAngle > MaxAngNW:
                BallAngle = MaxAngNW
            elif BallAngle > 0 and BallAngle < MaxAngSW:
                BallAngle = MaxAngSW
            Left2Right = False
            BallSpeed = LBallSpeed

#Left Paddle Edge Detection
    xDelta = LPaddleEdgeX-(BallX-BallRadius) #Gap between right edge of paddle and left edge of the ball
    yDelta = LPaddleY+LPaddleHHalf-BallY #Gap between middle of paddle and middle of the ball.  Note if - then ball is below center
    if not LPast and xDelta >= 0:
        LPast = True # This is the first time the ball got past or hit us.
                     # This 'saves' the ball if the speed is fast enough to go from the
                     # left side of the paddle to being past the paddle.
        RPast = False
        if abs(yDelta)<(LPaddleHHalf+BallRadius):
            if (LPaddleEdgeX-BallX)<BallRadius:
                BallX = ((BallRadius+LPaddleEdgeX)<<1)-BallX #Similar to above where ball moved past the paddle so now we keep it always right of the paddle
            PadPercent = yDelta/(LPaddleHHalf+BallRadius)
            if BallAngle > 0:
                m1 = math.pi
            else:
                m1 = -math.pi
            BallAngle = m1-BallAngle-(dAngMax*PadPercent)
            #BallAngle needs to be bounded min(max(BallAngle,MAXANGNE),MAXANGSE)
            if BallAngle < MaxAngNE:
                BallAngle = MaxAngNE
            elif BallAngle > MaxAngSE:
                BallAngle = MaxAngSE
            Left2Right = True
            BallSpeed = RBallSpeed       
     

    screen.fill(WHITE)
#    screen.blit(TextDImg, (10,500))
    TextImg = MyFont.render(str(RScore).zfill(2),True,BLUE, WHITE)
    screen.blit(TextImg, (ScoreRX,ScoreY))
    TextImg = MyFont.render(str(LScore).zfill(2),True,GREEN, WHITE)
    screen.blit(TextImg, (ScoreLX,ScoreY))
    pygame.draw.rect(screen, BLACK, (NetL,0,NetW,ScreenHeight))
    pygame.draw.circle(screen, RED, BallLocation, BallRadius)
    pygame.draw.rect(screen, BLUE, RPaddle)
    pygame.draw.rect(screen, GREEN, LPaddle)
    screen.blit(TextMsg, (ScreenWidth/3,ScreenHeight/2))

    pygame.display.update()
    time.sleep(0.01)
            
print ("Game Over")

pygame.quit()
