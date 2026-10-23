import pygame
from CONSTANTS import *

pygame.init()
screen = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)


cube_dictionary = {}

class Cube:
    def __init__(self, x_offset, y_offset, z_offset, w=CUBE_SIZE, h=CUBE_SIZE, row=0, file=0, col = 0, image = WHITE_CUBE_IMAGE):
        self.width = w
        self.height = h
        self.x = (file - row - 1) * w * 0.5
        self.y = (file + row) * h * 0.25
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z = z_offset
        self.row = row
        self.file = file
        self.col = col
        self.image = image

    def draw(self):
        screen.blit(self.image, (self.x + self.x_offset, self.y + self.y_offset - self.z - self.col * CUBE_SIZE))

class Map:

    def __init__(self, number_of_cubes, number_of_layers, gap_size=1):
        self.number_of_cubes = number_of_cubes
        self.number_of_layers = number_of_layers
        self.gap_size = gap_size
        self.cube_dict = {}
        for row in range(self.number_of_cubes):
            for file in range(self.number_of_cubes):
                for col in range(0, self.number_of_layers * self.gap_size, self.gap_size):
                    self.cube_dict[row, file, col] = Cube(screen.get_width()/2, (screen.get_height() - TOTAL_GRID_HEIGHT)/2, 0, CUBE_SIZE, CUBE_SIZE, row, file, col*0.5, WHITE_CUBE_IMAGE)
        print(self.cube_dict)

    def draw(self):
        for coord, cube in self.cube_dict.items():
            cube.x_offset = screen.get_width()/2
            cube.y_offset = ( screen.get_height() - TOTAL_GRID_HEIGHT ) /2
            cube.draw()


#create_grid(NUMBER_OF_CUBES)
grid = Map(NUMBER_OF_CUBES, NUMBER_OF_LAYERS, 1)
coords = [0,0,NUMBER_OF_LAYERS-1]
cube1 = Cube(screen.get_width()/2,(screen.get_height() - TOTAL_GRID_HEIGHT)/2, 0, CUBE_SIZE, CUBE_SIZE, 0, 0, NUMBER_OF_CUBES-1, RED_CUBE_IMAGE)
cube1.z = cube1.height*0.5

print(cube_dictionary)

while True:
    screen.fill((100, 150, 100))
    #draw_grid()
    grid.draw()
    cube1.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(cube_dictionary)
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print(coords)
                coords[0] -= 1
                if (coords[0], coords[1], coords[2]) not in cube_dictionary:
                    coords[0] += 1
            elif event.key == pygame.K_DOWN:
                print(coords)
                coords[0] += 1
                if (coords[0], coords[1], coords[2]) not in cube_dictionary:
                    coords[0] -= 1
            elif event.key == pygame.K_LEFT:
                print(coords)
                coords[1] -= 1
                if (coords[0], coords[1], coords[2]) not in cube_dictionary:
                    coords[1] += 1
            elif event.key == pygame.K_RIGHT:
                print(coords)
                coords[1] += 1
                if (coords[0], coords[1], coords[2]) not in cube_dictionary:
                    coords[1] -= 1

    """
    cube1.x = cube_dictionary[coords[0], coords[1], coords[2]].x
    cube1.x_offset = screen.get_width()/2
    cube1.y = cube_dictionary[coords[0], coords[1], coords[2]].y
    cube1.y_offset = (screen.get_height() - TOTAL_GRID_HEIGHT) /2
    """

    cube1.x = grid.cube_dict[coords[0], coords[1], coords[2]].x
    cube1.x_offset = screen.get_width() / 2
    cube1.y = grid.cube_dict[coords[0], coords[1], coords[2]].y
    cube1.y_offset = (screen.get_height() - TOTAL_GRID_HEIGHT) / 2


    pygame.display.flip()
    CLOCK.tick(60)


