import pygame
from pygame.locals import *
import math
import random
import sys
import time as time

pygame.init()
clock = pygame.time.Clock()

w = 800
h = 600
hi = 600

window = pygame.display.set_mode((w,h))
pygame.display.set_caption("Winky McWinkerson")

ds = pygame.display.set_mode((w,h))

black = (0,0,0)
white = (255,255,255)

bg = pygame.image.load("grass.png").convert()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((w/2),(h/2))
    ds.blit(TextSurf, TextRect)
    pygame.display.update()

def detectCollisions(x1,y1,w1,h1,x2,y2,w2,h2):
    if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    else:
        return False

class Sprite:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width = width
        self.height = height
        self.image = pygame.image.load("piney.jpg")
    def render(self,collision):
        if (collision == True): # make them red when there's a collision
            message_display("game ova!!!")
            pygame.time.delay(3000)
            pygame.display.quit()
            pygame.quit()
            sys.exit

        else:
            ds.blit(self.image, (self.x, self.y))
        if (self.y + self.height >= 600):
            self.y = 0
            # randomize x position between 50 and 650 in 50px intervals
            self.x = random.randint(1,12)*50

            # randomize start positions
            startx1=random.randint(1,12)*50
            startx2=random.randint(1,12)*50
            startx3=random.randint(1,12)*50
            startx4=random.randint(1,12)*50
            # make those obstacles woooo ~ (x,y,width,height)
            # have them all start @ the top of the screen
            obstacle1=Sprite(startx1,100,100,100)
            obstacle2=Sprite(startx2,50,100,100)
            obstacle3=Sprite(startx3,150,100,100)
            obstacle4=Sprite(startx4,200,100,100)


# make those obstacles woooo ~~~ (x,y,width,height)
# have them all start @ the top of the screen
obstacle1=Sprite(50,100,51,93)
obstacle2=Sprite(200,50,51,93)
obstacle3=Sprite(350,150,51,93)
obstacle4=Sprite(500,200,51,93)

dude=Sprite(350,350,100,100) # doodie @ bottom
moveX,moveY=0,0 # for dude
obstaclesMoving = 0 # for obstacles -- going to have to decrease Y position

gameLoop = True

while gameLoop:

    for event in pygame.event.get():

        # end game
        if (event.type==pygame.QUIT):
            gameLoop=False # bye bye
            # add a bye bye msg

        # FOR DUDE MOVEMENTS -----------------------------------
        if (event.type==pygame.KEYDOWN): # when a key is pressed...
            # determine which key
            # only dude can move side to side with the keys
            if (event.key==pygame.K_LEFT):
                moveX = -4 # move x direction negative aka LARRY
            if (event.key==pygame.K_RIGHT):
                moveX = 4 # move x direction positive aka RANDOLPH
            if (event.key==pygame.K_UP):
                moveY = 0 # not allowed to move up
            if (event.key==pygame.K_DOWN):
                moveY = 0 # not allowed to move down
        if (event.type==pygame.KEYUP): # when a key is let go
            # do nothin lol this is kind of unnecessary
            if (event.key==pygame.K_LEFT):
                moveX=0
            if (event.key==pygame.K_RIGHT):
                moveX=0
            if (event.key==pygame.K_UP):
                moveY=0
            if (event.key==pygame.K_DOWN):
                moveY=0
        # ------------------------------------------------------

    # FOR OBSTACLE MOVEMENT & GENERATION -----------------------
    # (do not rely on events!!! need to happen based on time)
    # they have to continuously move forward at the same rate
    if (time.time() % 1 != 0): # not sure why I have to do this weirdly but w/e
        obstaclesMoving = 3 # maybe have this var change later based on time passed
        obstacle1.y+=obstaclesMoving
        obstacle2.y+=obstaclesMoving
        obstacle3.y+=obstaclesMoving
        obstacle4.y+=obstaclesMoving

    rel_y = hi % bg.get_rect().height
    ds.blit(bg, (0, rel_y - bg.get_rect().height))
    hi += 3

    #window.fill(white)
    dude.x+=moveX # update x
    dude.y+=moveY # update y
    # see if new position collides with standing still sprite dude
    collisions1=detectCollisions(obstacle1.x,obstacle1.y,obstacle1.width,obstacle1.height,dude.x,dude.y,dude.width,dude.height)
    collisions2=detectCollisions(obstacle2.x,obstacle2.y,obstacle2.width,obstacle2.height,dude.x,dude.y,dude.width,dude.height)
    collisions3=detectCollisions(obstacle3.x,obstacle3.y,obstacle3.width,obstacle3.height,dude.x,dude.y,dude.width,dude.height)
    collisions4=detectCollisions(obstacle4.x,obstacle4.y,obstacle4.width,obstacle4.height,dude.x,dude.y,dude.width,dude.height)

    # obstacle colour always stays same so we send false
    obstacle1.render(collisions1)
    obstacle2.render(collisions2)
    obstacle3.render(collisions3)
    obstacle4.render(collisions4)
    # standing still dude changes colour if they hit an obstacle
    dude.render(False)
    pygame.display.flip()
    clock.tick(50)



pygame.quit()
