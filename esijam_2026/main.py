from random import randint
from CONSTANTS import *

pygame.init()
screen = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)

class Cube:
    def __init__(self, x_offset, y_offset, z_offset, row=0, file=0, col = 0, image = WHITE_CUBE_IMAGE):
        self.row = row
        self.file = file
        self.col = col
        self.x = (file - self.row - 1) * CUBE_SIZE * 0.5
        self.y = (file + self.row) * CUBE_SIZE * 0.25
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z = z_offset
        self.image = image

    """
    def random_drop(self):
        self.row = randint(0, NUMBER_OF_CUBES - 1)
        self.file = randint(0, NUMBER_OF_CUBES - 1)
        self.col = randint(0, NUMBER_OF_LAYERS - 1)
        self.z = 100
        #100, randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_CUBES), BLUE_CUBE_IMAGE)
    """

    def draw(self):
        screen.blit(self.image, (self.x + self.x_offset, self.y + self.y_offset - self.z - self.col * GAP_SIZE * CUBE_SIZE * 0.5))

class Map:
    def __init__(self):
        self.cube_dict = {}
        for row in range(NUMBER_OF_CUBES):
            for file in range(NUMBER_OF_CUBES):
                for col in range(NUMBER_OF_LAYERS):
                    self.cube_dict[row, file, col] = Cube(screen.get_width()/2, (screen.get_height() - TOTAL_GRID_HEIGHT)/2, 0, row, file, col, WHITE_CUBE_IMAGE)

    def draw(self):
        for row in range(NUMBER_OF_CUBES):
            for file in range(NUMBER_OF_CUBES):
                for col in range(NUMBER_OF_LAYERS+1):
                    cube = self.cube_dict.get((row, file, col))
                    if cube:
                        cube.draw()
        """
        for coord, cube in self.cube_dict.items():
            cube.x_offset = screen.get_width()/2
            cube.y_offset = ( screen.get_height() - TOTAL_GRID_HEIGHT ) /2
            cube.draw()
        """




#create_grid(NUMBER_OF_CUBES)
grid = Map()

coords = [0,0,TOP_LAYER]
cube1 = Cube(screen.get_width()/2, (screen.get_height() - TOTAL_GRID_HEIGHT)/2, CUBE_SIZE*0.5, 0, 0, TOP_LAYER, RED_CUBE_IMAGE)

cube = Cube(screen.get_width() / 2, (screen.get_height() - TOTAL_GRID_HEIGHT) / 2, 100, randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_LAYERS), BLUE_CUBE_IMAGE)

while True:
    screen.fill((100, 150, 100))
    grid.draw()
    cube1.draw()
    if cube.z > 0 + CUBE_SIZE*0.5:
        cube.z -= 1
        cube.draw()
    else:
        grid.cube_dict[cube.row, cube.file, cube.col+1] = cube
        cube = Cube(screen.get_width() / 2,(screen.get_height() - TOTAL_GRID_HEIGHT) / 2,100,randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_CUBES - 1),randint(0, NUMBER_OF_LAYERS - 1), BLUE_CUBE_IMAGE,)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                continue
            if event.key == pygame.K_UP:
                print(coords)
                coords[0] -= 1
                if (coords[0], coords[1], coords[2]) not in grid.cube_dict:
                    coords[0] += 1
            elif event.key == pygame.K_DOWN:
                print(coords)
                coords[0] += 1
                if (coords[0], coords[1], coords[2]) not in grid.cube_dict:
                    coords[0] -= 1
            elif event.key == pygame.K_LEFT:
                print(coords)
                coords[1] -= 1
                if (coords[0], coords[1], coords[2]) not in grid.cube_dict:
                    coords[1] += 1
            elif event.key == pygame.K_RIGHT:
                print(coords)
                coords[1] += 1
                if (coords[0], coords[1], coords[2]) not in grid.cube_dict:
                    coords[1] -= 1


    cube1.x = grid.cube_dict[coords[0], coords[1], coords[2]].x
    cube1.x_offset = screen.get_width() / 2
    cube1.y = grid.cube_dict[coords[0], coords[1], coords[2]].y
    cube1.y_offset = (screen.get_height() - TOTAL_GRID_HEIGHT) / 2


    pygame.display.flip()
    CLOCK.tick(60)


