from shutil import move
from numpy import radians
from sympy import python
import pygame
import math
import time
import os
from utils import scale_img, draw_img, blit_rotate_center


GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 1.2)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.6)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"),0.6)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load("imgs/finish.png")
RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.5)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"), 0.5)

images = [
    (GRASS, (0, 0)),
    (TRACK, (0, 0)),
    # (RED_CAR, (50,50))
    # (GRASS, (0, 0))
]

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")
FPS = 60


class AbstractCar:
    def __init__(self, max_velo, rotation_velo):
        self.img = self.IMG
        self.max_velo = max_velo 
        self.velo = 0
        self.rotation_velo = rotation_velo
        self.angle = 0
        # The position represent by (x, y)
        self.x, self.y= self.START_POS
        self.acceleration= 0.1
    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_velo
        elif right:
            self.angle -= self.rotation_velo
    
    def draw(self, window):
        blit_rotate_center(window, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.velo = min(self.velo + self.acceleration, self.max_velo)
        self.move()

    def move_backward(self):
        self.velo = max(self.velo - self.acceleration, -self.max_velo/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        horizontal = math.sin(radians) * self.velo
        vertical = math.cos(radians) * self.velo

        self.y -= vertical
        self.x -= horizontal

    

    def collide(self, mask, x=0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
class PlayerCar(AbstractCar):
    IMG=RED_CAR
    START_POS = (180,200)

    def reduce_speed(self):
        self.velo = max(self.velo - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.velo = -self.velo
        self.move()

def player_move(player_car):
    keys = pygame.key.get_pressed()
    # IF not press key to move => moved = False => reduce speed
    moved = False

    # Watching if left and right btn triggered to 
    # do rotating
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

run = True
clock = pygame.time.Clock()
player_car = PlayerCar(4,4)

while run:

    clock.tick(FPS)

    draw_img(WINDOW, images, player_car) 

    pygame.display.update()

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            run = False
            break
    player_move(player_car)

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
        
    

pygame.quit()


