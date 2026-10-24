from numpy.f2py.symbolic import eliminate_quotes

from CONSTANTS import *

class Cube:
    def __init__(self, row, file, col, image = WHITE_CUBE_IMAGE, transparency = 255):
        self.row = row
        self.file = file
        self.col = col
        self.image = image
        self.transparency = transparency # (0 = invisible, 255 = fully opaque)
        self.z = 0

    def screen_position(self):
        x_offset = SCREEN.get_width() / 2
        y_offset = (SCREEN.get_height() - TOTAL_GRID_HEIGHT) / 2
        x_in_pixels = (self.file - self.row - 1) * CUBE_SIZE * 0.5 #(*0.5 : isometric maths)
        y_in_pixels = (self.file + self.row) * CUBE_SIZE * 0.25 #(*0.25 : isometric maths)
        layer_in_pixels = self.col * GAP_SIZE * CUBE_SIZE *0.5 #(*0.5 : isometric maths)

        screen_x = x_in_pixels + x_offset
        screen_y = y_in_pixels + y_offset - layer_in_pixels - self.z
        return screen_x, screen_y

    def draw(self):
        self.image.set_alpha(self.transparency)
        SCREEN.blit(self.image, self.screen_position())



class Player(Cube):
    def __init__(self, row, file, col, image):
        super().__init__(row, file, col, image)
        self.z = CUBE_SIZE * 0.5
        self.state = "alive"

    def move(self, d_row, d_file, d_col, grid):
        if self.state == "eliminated":
            return
        target_position = (self.row + d_row, self.file + d_file, self.col + d_col)
        if target_position in grid.cube_dict:
            self.row, self.file, self.col = target_position

    def draw(self):
        if self.state == "eliminated":
            return
        SCREEN.blit(self.image, self.screen_position())
