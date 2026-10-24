from random import randint
from CONSTANTS import *

pygame.init()
screen = pygame.display.set_mode(INITIAL_SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(CAPTION)

player_layer = 0


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
        self.layer = self.col * GAP_SIZE
        self.image = image
    """
    def drop(self):
        if self.z > 0 + CUBE_SIZE * 0.5:
            self.z -= 1
            self.draw()
        else:
            grid.cube_dict[self.row, self.file, self.col + 1] = self
            self = Cube(screen.get_width() / 2, (screen.get_height() - TOTAL_GRID_HEIGHT) / 2, 100,randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_CUBES - 1),randint(0, NUMBER_OF_LAYERS - 1), BLUE_CUBE_IMAGE, )
    """

    def draw(self):
        screen.blit(self.image, (self.x + self.x_offset, self.y + self.y_offset - self.z - self.layer * CUBE_SIZE * 0.5))

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
                    if [row, file, col] == coords:
                        cube1.draw()
        """
        for coord, cube in self.cube_dict.items():
            cube.x_offset = screen.get_width()/2
            cube.y_offset = ( screen.get_height() - TOTAL_GRID_HEIGHT ) /2
            cube.draw()
        """




#create_grid(NUMBER_OF_CUBES)
grid = Map()

coords = [0,0,player_layer+1]
cube1 = Cube(screen.get_width()/2, (screen.get_height() - TOTAL_GRID_HEIGHT)/2, CUBE_SIZE*0.5, 0, 0, player_layer, RED_CUBE_IMAGE)

#falling_cube = Cube(screen.get_width() / 2, (screen.get_height() - TOTAL_GRID_HEIGHT) / 2, 100, randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_LAYERS), BLUE_CUBE_IMAGE)

while True:
    screen.fill((100, 150, 100))
    grid.draw()
    #cube1.draw()

    #falling_cube.drop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:

            if event.key in MOVES:
                d_row,d_file,d_col = MOVES[event.key]
                target_position = (coords[0] + d_row, coords[1] + d_file, coords[2] - 1 + d_col) #coords[2]-1 : a cube exists to stand on
                if target_position in grid.cube_dict:
                    coords[0]+=d_row
                    coords[1]+=d_file
                    coords[2]+=d_col


            support = grid.cube_dict[coords[0], coords[1], coords[2] - 1]
            cube1.x = support.x
            cube1.y = support.y
            cube1.layer = support.layer
            cube1.x_offset = screen.get_width() / 2
            cube1.y_offset = (screen.get_height() - TOTAL_GRID_HEIGHT) / 2


    pygame.display.flip()
    CLOCK.tick(60)


