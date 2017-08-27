import math, random, sys
import pygame
from pygame.locals import *

# exit the program
def events():
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()

# define display surface
W, H = 800, 600
HW, HH = W / 2, H / 2
AREA = W * H

# initialise display
pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("code.Pylet - Template")
FPS = 50

# define some colors
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)

bg = pygame.image.load("grass.png").convert()
#biker = pygame.image.load("biker.png").convert
bgWidth, bgHeight = bg.get_rect().size

block = pygame.image.load("biker.gif").convert()
blockWidth, blockHeight = block.get_rect().size

blockbig = pygame.image.load("bikerbig.gif").convert()
blockbigWidth, blockbigHeight = blockbig.get_rect().size


startScrollingPosX = HW

circleRadius=25
circlePosX = 400
playerPosX = 400
playerPosy = 545
y=0

# main loop
while True:
	events()
	k = pygame.key.get_pressed()
	if k[K_RIGHT]:
		if playerPosX ==400 :
			playerPosX = 600
		elif playerPosX == 150:
			playerPosX = 400
		#playerPosX+=200
		#if playerPosX > 600:
			#playerPosX=600
	elif k[K_LEFT]:
		if playerPosX==400:
			playerPosX=150
		elif playerPosX==600:
			playerPosX=400
		#playerPosX-=125
		#if playerPosX<125:
			#playerPosX=125
	if playerPosX > W - circleRadius:
		playerPosX = W - circleRadius
	if playerPosX< circleRadius:
		playerPosX = circleRadius
	circlePosX = playerPosX

	rel_y = y % bg.get_rect().height
	DS.blit(bg, (0, rel_y - bg.get_rect().height))
	if rel_y < H:
		DS.blit(bg, (0, rel_y))
	y += 3
	if k[K_SPACE]:
		DS.blit(blockbig,(circlePosX, playerPosy - blockHeight))
	else:
		DS.blit(block,(circlePosX, playerPosy - blockHeight))

	#pygame.draw.circle(DS,WHITE,(circlePosX, playerPosy - circleRadius), circleRadius, 0)
	pygame.display.update()
	CLOCK.tick(FPS)
	DS.fill(BLACK)
