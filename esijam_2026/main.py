import pygame
from CONSTANTS import *

pygame.init()
screen = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)

cube_image = pygame.image.load(f'images/white_cube.png')

class Cube:
    def __init__(self, x_offset, y_offset, w=16, h=16, row=0, col=0):
        self.width = w
        self.height = h
        self.x = (col - row - 1) * w * 0.5 + x_offset
        self.y = (col + row) * h * 0.25 + y_offset
        self.row = row
        self.col = col

    def draw(self):
        scaled_cube = pygame.transform.scale(cube_image, (int(self.width), int(self.height)))
        screen.blit(scaled_cube, (self.x, self.y))

def draw_grid(number_of_cubes):
    screen_width, screen_height = screen.get_size()
    cube_width = 50
    cube_height = 50
    total_grid_width = number_of_cubes * cube_width
    total_grid_height = number_of_cubes * cube_height * 0.5
    x_offset = screen_width /2
    y_offset = (screen_height - total_grid_height) /2

    for row in range(number_of_cubes):
        for col in range(number_of_cubes):
            cube = Cube(x_offset, y_offset, cube_width, cube_height, row, col)
            cube.draw()


while True:
    screen.fill((100, 150, 100))
    screen_width, screen_height = screen.get_size()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #cube1 = Cube(screen_width/2,screen_height/2, 50, 50)
    #cube1.draw()
    draw_grid(5)

    pygame.display.flip()