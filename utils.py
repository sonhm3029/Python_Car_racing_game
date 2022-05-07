import pygame

def scale_img(img, factor):

    size = round(img.get_width()* factor), round(img.get_width() * factor)
    return pygame.transform.scale(img, size)

def draw_img(window, images, player_car):
    for img, position in images:
        window.blit(img, position)
    player_car.draw(window)
    pygame.display.update()

def blit_rotate_center(window, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    window.blit(rotated_image, new_rect.topleft)


