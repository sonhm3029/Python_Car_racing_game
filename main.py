from shutil import move
from numpy import radians
from sympy import python
import pygame
import math
import time
import os
from utils import scale_img, draw_img, blit_rotate_center


GRASS = scale_img(pygame.image.load("imgs/grass.jpg"), 1.6)
TRACK = scale_img(pygame.image.load("imgs/track.png"), 0.7)
TRACK_BORDER = scale_img(pygame.image.load("imgs/track-border.png"),0.7)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = scale_img(pygame.image.load("imgs/finish.png"),0.7)
FINISH_POSITION = (100,200)
FINISH_MASK = pygame.mask.from_surface(FINISH)


RED_CAR = scale_img(pygame.image.load("imgs/red-car.png"), 0.4)
GREEN_CAR = scale_img(pygame.image.load("imgs/green-car.png"), 0.4)


images = [
    (GRASS, (0, 0)),
    (TRACK, (0, 0)),
    (FINISH, FINISH_POSITION),
    (TRACK_BORDER, (0,0))
    # (RED_CAR, (50,50))
    # (GRASS, (0, 0))
]

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WINDOW= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")
FPS = 60
SOLVE_PATH = [(134, 86), (76, 48), (47, 88), (48, 363), (263, 573), (325, 514), (325, 400), (395, 371), (470, 434), (480, 564), (570, 566), (563, 
313), (495, 284), (314, 264), (328, 199), (545, 203), (579, 93), (431, 57), (229, 65), (208, 302), (144, 303), (138, 209)]


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

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.velo = 0
class PlayerCar(AbstractCar):
    IMG=RED_CAR
    START_POS = (120,165)

    def reduce_speed(self):
        self.velo = max(self.velo - self.acceleration/2, 0)
        self.move()

    def bounce(self):
        self.velo = -self.velo
        self.move()


class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (140,165)

    def __init__(self, max_velo, rotation_velo, path=[]):
        super().__init__(max_velo, rotation_velo)
        self.path = path
        self.current_point = 0
        self.velo = max_velo

    def draw_points(self, window):
        for point in self.path:
            pygame.draw.circle(window, (255,0,0), point, 5)

    def draw(self, window):
        super().draw(window)
        # self.draw_points(window)
    
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        # desired_radian_angle = 0

        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)
        if target_y > self.y:
            desired_radian_angle += math.pi
        
        diff_in_angle = self.angle - math.degrees(desired_radian_angle)

        if diff_in_angle >=180:
            diff_in_angle -= 360
        if diff_in_angle > 0:
            self.angle -= min(self.rotation_velo, abs(diff_in_angle))
        else:
            self.angle += min(self.rotation_velo, abs(diff_in_angle))
    
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point +=1

    def move(self):
        if self.current_point >= len(self.path):
            return
        self.calculate_angle()
        self.update_path_point()
        super().move()


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
computer_car = ComputerCar(1,4, SOLVE_PATH)

while run:

    clock.tick(FPS)

    draw_img(WINDOW, images, player_car, computer_car) 

    pygame.display.update()

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            run = False
            break
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     computer_car.path.append(pos)

    player_move(player_car)

    if len(SOLVE_PATH) >0:
        computer_car.move()
    

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_po_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_po_collide != None:
        print("Computer win !") 
        computer_car.reset()
        player_car.reset()


    player_finish_po_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if  player_finish_po_collide !=None:
        if player_finish_po_collide[1] == 0:
            player_car.bounce()
        else :
            player_car.reset()
            computer_car.reset()
        
    
pygame.quit()


