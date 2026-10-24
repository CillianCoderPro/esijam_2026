from CONSTANTS import *
from Cube import Cube

class Grid:
    def __init__(self):
        self.cube_dict = {}
        for row in range(NUMBER_OF_CUBES):
            for file in range(NUMBER_OF_CUBES):
                for col in range(NUMBER_OF_LAYERS):
                    self.cube_dict[row, file, col] = Cube(row, file, col)

    def draw(self, player):
        for row in range(NUMBER_OF_CUBES):
            for file in range(NUMBER_OF_CUBES):
                for col in range(NUMBER_OF_LAYERS+1):
                    cube = self.cube_dict.get((row, file, col))
                    if cube:
                        cube.draw()
                    if (row, file, col) == (player.row, player.file, player.col+1):
                        player.draw()