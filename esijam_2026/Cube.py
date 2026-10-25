from CONSTANTS import *

class Cube:
    def __init__(self, row, file, col, image = WHITE_CUBE_IMAGE, transparency = 255):
        self.row = row
        self.file = file
        self.col = col
        self.image = image
        self.transparency = transparency # (0 = invisible, 255 = fully opaque)
        self.z = 0
        self.broken_state_number = 0
        self.frame_timer = 0
        self.broken = False

    def step_on(self):
        """Called once, the moment a player arrives on this cube."""
        if self.broken_state_number == NUMBER_OF_GRID_CUBE_IMAGES-1:
            self.broken = True
        else:
            self.broken_state_number = self.broken_state_number+1
            self.frame_timer = 0

    def update_broken_state(self):
        """Called every frame while the player is on this cube"""
        self.frame_timer += 1
        if self.frame_timer >= FRAMES_BEFORE_CUBE_BREAKS:
            self.frame_timer = 0
            if self.broken_state_number < NUMBER_OF_GRID_CUBE_IMAGES-1:
                self.broken_state_number += 1
            else:
                self.broken = True

    def is_broken(self): return self.broken

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
        print(self.broken_state_number)
        self.image = GRID_CUBE_IMAGES[self.broken_state_number]
        #self.image.set_alpha(self.transparency)
        SCREEN.blit(self.image, self.screen_position())



class Player(Cube):
    def __init__(self, row, file, col, image):
        super().__init__(row, file, col, image)
        self.z = CUBE_SIZE * 0.5
        self.state = "alive"
        self.current_cube = None

    def update_state(self, grid):
        if  self.state == "eliminated":
            return

        immediate_current_cube = grid.cube_dict.get((self.row, self.file, self.col))

        if not immediate_current_cube:
            self.state = "eliminated"
            return

        if immediate_current_cube != self.current_cube: #if player has just arrived at a new cube
            self.current_cube = immediate_current_cube
            self.current_cube.step_on()
        elif self.current_cube.is_broken():
            grid.cube_dict.pop((self.row, self.file, self.col))
            self.col -= 1
        else:
            self.current_cube.update_broken_state()


    def move(self, d_row, d_file, d_col, grid, list_of_players):
        if self.state == "eliminated":
            return

        target_position = (self.row + d_row, self.file + d_file, self.col + d_col)

        for player in list_of_players:
            if target_position == (player.row, player.file, player.col):
                return
        if target_position in grid.cube_dict:
            self.row, self.file, self.col = target_position


    def draw(self):
        if self.state == "eliminated":
            return
        SCREEN.blit(self.image, self.screen_position())



