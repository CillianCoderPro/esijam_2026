from CONSTANTS import *
from Cube import Cube

class Grid:
    def __init__(self):
        self.cube_dict = {}
        for row in range(NUMBER_OF_CUBES):
            for file in range(NUMBER_OF_CUBES):
                for col in range(NUMBER_OF_LAYERS):
                    self.cube_dict[row, file, col] = Cube(SCREEN.get_width() / 2, (SCREEN.get_height() - TOTAL_GRID_HEIGHT) / 2, 0, row, file, col, WHITE_CUBE_IMAGE)

    def draw(self, coords, player):
        for row in range(NUMBER_OF_CUBES):
            for file in range(NUMBER_OF_CUBES):
                for col in range(NUMBER_OF_LAYERS+1):
                    cube = self.cube_dict.get((row, file, col))
                    if cube:
                        cube.draw()
                    if [row, file, col] == coords:
                        player.draw()