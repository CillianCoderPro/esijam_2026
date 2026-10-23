import pygame
from CONSTANTS import *

pygame.init()
screen = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)


cube_dictionary = {}

class Cube:
    def __init__(self, x_offset, y_offset, w=16, h=16, row=0, col=0, z=0, image = WHITE_CUBE_IMAGE):
        self.width = w
        self.height = h
        self.x = (col - row - 1) * w * 0.5 + x_offset
        self.y = (col + row) * h * 0.25 + y_offset
        self.row = row
        self.col = col
        self.image = image
        self.z = z

    def draw(self):
        screen.blit(self.image, (self.x, self.y - self.z))

def create_grid(number_of_cubes):
    screen_width, screen_height = screen.get_size()
    cube_width = 50
    cube_height = 50
    total_grid_width = number_of_cubes * cube_width
    total_grid_height = number_of_cubes * cube_height * 0.5
    x_offset = screen_width /2
    y_offset = (screen_height - total_grid_height) /2

    for row in range(number_of_cubes):
        for col in range(number_of_cubes):
            cube = Cube(x_offset, y_offset, cube_width, cube_height, row, col, 0, WHITE_CUBE_IMAGE)
            cube_dictionary[row, col] = cube


def draw_grid():
    for key, cube in cube_dictionary.items():
        cube.draw()

create_grid(10)
coords = [0,0]
cube1 = cube_dictionary[coords[0], coords[1]]
cube1.image = RED_CUBE_IMAGE
cube1.z = cube1.height*0.5

while True:
    screen.fill((100, 150, 100))
    draw_grid()
    cube1.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print(coords)
                coords[0] -= 1
                if (coords[0], coords[1]) not in cube_dictionary:
                    coords[0] += 1
            elif event.key == pygame.K_DOWN:
                coords[0] += 1
                if (coords[0], coords[1]) not in cube_dictionary:
                    coords[0] -= 1
            elif event.key == pygame.K_LEFT:
                coords[1] -= 1
                if (coords[0], coords[1]) not in cube_dictionary:
                    coords[1] += 1
            elif event.key == pygame.K_RIGHT:
                coords[1] += 1
                if (coords[0], coords[1]) not in cube_dictionary:
                    coords[1] -= 1

    cube1.x = cube_dictionary[coords[0], coords[1]].x
    cube1.y = cube_dictionary[coords[0], coords[1]].y

    pygame.display.flip()
    CLOCK.tick(60)

