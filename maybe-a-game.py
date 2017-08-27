import pygame
from pygame.locals import *
import math
import random
import sys
import time as time
import numpy as np
import cv2

########################
#In the first part of the code we train the face cascade with the xml file.
face_cascade= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade= cv2.CascadeClassifier('haarcascade_eye.xml')

#Start capturing video
cap=cv2.VideoCapture(0)


leftWink=False
leftWinkCounter=0
rightWink=False
rightWinkCounter=0
blinkWink=False
blinkWinkCounter=0
########################

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
        if x == 111 and y == 111:
            self.image = pygame.image.load("mrpoopybutthole.jpg")
            self.x = 350
            self.y = 350
        else:
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

dude=Sprite(111,111,50,102) # doodie @ bottom
moveX,moveY=0,0 # for dude
obstaclesMoving = 0 # for obstacles -- going to have to decrease Y position

gameLoop = True

while gameLoop:

    ####################################
    #These return a true/false if the frame is read correctly
    ret,frame=cap.read()

    #Convert the frame to grayscale so we can analyze it using a Haar cascade
    grayFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Now, find faces in the image

    #Faces are returned as a list of rectangles: Rect(x,y,w,h)
    faces = face_cascade.detectMultiScale(grayFrame, 1.3, 5)
    #########################################


    for(x,y,w,h) in faces:

        #Draw a box around the face.
        cv2.rectangle(frame,(x,y),(x+w,y+h), (255,0,0),2)
        #Find eyes now cause they're always in the face
        #We input the grey region of interest (the rectange that the face we are looping for)


        #right eye first
        rightGrayROI= grayFrame[y:y+(h/2), x:x+(w/2)]
        rightColourROI=frame[y:y+(h/2),x:x+(w/2)]
        rightEye=eye_cascade.detectMultiScale(rightGrayROI)

        leftGrayROI= grayFrame[y:y+(h/2),(x+(w/2)):x+w]
        leftColourROI=frame[y:y+(h/2),(x+(w/2)):x+w]
        leftEye=eye_cascade.detectMultiScale(leftGrayROI)


        if  (not len(leftEye) and not len(rightEye)):
            blinkWink=True
            blinkWinkCounter+=1
            print "BLINK WINK COUNTER: " + str(blinkWinkCounter)
            if (blinkWinkCounter>10):
                print "blink"


        else:
            blinkWink=False
            blinkWinkCounter=0
            if not len(leftEye):
                leftWink=True
                leftWinkCounter+=1
                print leftWinkCounter
                if (leftWinkCounter>3):
                    print "left wink"
                    moveX = -4

            else:
                leftWink=False
                leftWinkCounter=0

            if not len(rightEye):
                rightWink=True
                rightWinkCounter+=1
                print rightWinkCounter
                if (rightWinkCounter>3):
                    print "right wink"
                    moveX = 4
            else:
                rightWink=False
                rightWinkCounter=0

        #Draw eye rectangles
        for (ex,ey,ew,eh) in rightEye:
            cv2.rectangle(rightColourROI,(ex,ey),(ex+ew,ey+eh),(0,120,120),2)

        for (ex,ey,ew,eh) in leftEye:
            cv2.rectangle(leftColourROI,(ex,ey),(ex+ew,ey+eh),(0,0,120),2)


    for event in pygame.event.get():

        # end game
        if (event.type==pygame.QUIT):
            gameLoop=False # bye bye
            # add a bye bye msg

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
#Release the capture, destroy windows.
cap.release()
cv2.destroyAllWindows()
