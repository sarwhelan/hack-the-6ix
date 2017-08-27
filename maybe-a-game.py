import pygame
from pygame.locals import *
import time as time

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Winky McWinkerson")

black = (0,0,0)
white = (255,255,255)
red = (255,25,25)


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

#def generateObstacle(x,y,width,height):


class Sprite:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width = width
        self.height = height
    def render(self,collision):
        if (collision == True): # make them red when there's a collision
            pygame.draw.rect(window,red,(self.x,self.y,self.width,self.height))
        else:
            pygame.draw.rect(window,black,(self.x,self.y,self.width,self.height))
        if (self.y + self.height >= 600):
            self.y = 0


# make those obstacles woooo ~~~ (x,y,width,height)
# have them all start @ the top of the screen
obstacle1=Sprite(50,100,100,100)
obstacle2=Sprite(200,50,100,100)
obstacle3=Sprite(350,150,100,100)
obstacle4=Sprite(500,200,100,100)
obstacle5=Sprite(650,150,100,100)

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
        obstaclesMoving = 2 # maybe have this var change later based on time passed
        obstacle1.y+=obstaclesMoving
        obstacle2.y+=obstaclesMoving
        obstacle3.y+=obstaclesMoving
        obstacle4.y+=obstaclesMoving
        obstacle5.y+=obstaclesMoving

    window.fill(white)
    dude.x+=moveX # update x
    dude.y+=moveY # update y
    # see if new position collides with standing still sprite dude
    collisions=detectCollisions(obstacle1.x,obstacle1.y,obstacle1.width,obstacle1.height,dude.x,dude.y,dude.width,dude.height)
    # obstacle colour always stays same so we send false
    obstacle1.render(False)
    obstacle2.render(False)
    obstacle3.render(False)
    obstacle4.render(False)
    obstacle5.render(False)
    # standing still dude changes colour if they hit an obstacle
    dude.render(collisions)
    pygame.display.flip()
    clock.tick(50)



pygame.quit()
