from sympy import python
import pygame
import math
import time
import os


GRASS = pygame.image.load("imgs/grass.jpg")
TRACK = pygame.image.load("imgs/track.png")
TRACK_BORDER = pygame.image.load("imgs/track-border.png")
FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = pygame.image.load("imgs/red-car.png")
GREEN_CAR = pygame.image.load("imgs/green-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()*0.5

WINDOW= pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Racing Game!")

FPS = 60

run = True
clock = pygame.time.Clock()

while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            run = False
            break

pygame.quit()


