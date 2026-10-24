from CONSTANTS import *

class Cube:
    def __init__(self, x_offset, y_offset, z_offset, row=0, file=0, col = 0, image = WHITE_CUBE_IMAGE):
        self.row = row
        self.file = file
        self.col = col
        self.x = (file - self.row - 1) * CUBE_SIZE * 0.5 #isometric maths
        self.y = (file + self.row) * CUBE_SIZE * 0.25 #isometric maths
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
        SCREEN.blit(self.image, (self.x + self.x_offset, self.y + self.y_offset - self.z - self.layer * CUBE_SIZE * 0.5))
