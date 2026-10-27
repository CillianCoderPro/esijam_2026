from CONSTANTS import *
import bots.random_square_bot
import bots.strongest_closest_square_bot

class Cube:
    def __init__(self, row, file, col, image = WHITE_CUBE_IMAGE, transparency = 255):
        self.row = row
        self.file = file
        self.col = col
        self.image = image
        self.transparency = transparency # (0 = invisible, 255 = fully opaque)

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


class GridCube(Cube):
    def __init__(self, row, file, col, image = WHITE_CUBE_IMAGE, transparency = 255):
        super().__init__(row, file, col, image, transparency)
        self.z = 0
        self.broken_state_number = 0
        self.frame_timer = 0
        self.broken = False

    def step_on(self):
        """Called once, the moment a player arrives on this cube."""
        if self.broken_state_number == NUMBER_OF_GRID_CUBE_IMAGES-1:
            self.broken = True
        else:
            self.broken_state_number += 1
            self.frame_timer = 0
        #if self.frame_timer > 1:
        self.image = GRID_CUBE_IMAGES[self.broken_state_number]

    def update_broken_state(self):
        """Called every frame while the player is on this cube"""
        self.frame_timer += 1
        if self.frame_timer == FRAMES_BEFORE_CUBE_BREAKS:
            self.frame_timer = 0
            if self.broken_state_number < NUMBER_OF_GRID_CUBE_IMAGES-1:
                self.broken_state_number += 1
            else:
                self.broken = True
                #BREAK_SOUND.play()
        self.image = GRID_CUBE_IMAGES[self.broken_state_number]

    def is_broken(self):
        return self.broken


class Player(Cube):
    def __init__(self, row, file, col, image, player_name):
        super().__init__(row, file, col, image)
        self.z = CUBE_SIZE * 0.5
        self.state = "alive"
        self.current_cube = None
        self.player_name = player_name
        self.distance_fallen = 0
        self.velocity = 0

    def update_falling_state(self, cube_below, number_of_layer_drops):
        if self.state != "falling":
            return
        pixels_between_layers = GAP_SIZE * CUBE_SIZE * 0.5 *  number_of_layer_drops # pixels between layers
        self.velocity += GRAVITY
        self.distance_fallen += self.velocity
        if self.distance_fallen >= pixels_between_layers and cube_below:
            self.distance_fallen = 0
            self.velocity = 0
            self.state = "alive"
            self.z = CUBE_SIZE * 0.5
            self.col -= number_of_layer_drops
        else:
            self.z = CUBE_SIZE * 0.5 - self.distance_fallen

    def update_state(self, grid):
        if  self.state == "eliminated":
            return
        if self.state == "falling":
            for i in range(1, NUMBER_OF_LAYERS+1):
                cube_below = grid.cube_dict.get((self.row, self.file, self.col - i))
                if cube_below:
                    self.update_falling_state(cube_below, i)
                    break
            else: # if there is no layer to fall to
                self.velocity += GRAVITY
                self.distance_fallen += self.velocity
                self.z = CUBE_SIZE * 0.5 - self.distance_fallen
                if self.distance_fallen >= SCREEN.get_height():
                    self.state = "eliminated"
            return

        immediate_current_cube = grid.cube_dict.get((self.row, self.file, self.col))
        """if not immediate_current_cube:
            self.state = "eliminated"
            return"""
        if immediate_current_cube != self.current_cube: #if player has just arrived at a new cube
            self.current_cube = immediate_current_cube
            self.current_cube.step_on()
        elif self.current_cube.is_broken(): #if cube has just been broken
            BREAK_SOUND.play()
            grid.cube_dict.pop((self.row, self.file, self.col))
            self.state = "falling"
        else:
            self.current_cube.update_broken_state()


    def move(self, d_row, d_file, d_col, grid, list_of_players):
        if self.state == "eliminated":
            return
        target_position = (self.row + d_row, self.file + d_file, self.col + d_col)
        for player in list_of_players:
            if target_position == (player.row, player.file, player.col) and player.state != "eliminated": # collision
                return
        if target_position in grid.cube_dict:
            self.row, self.file, self.col = target_position

    def draw(self):
        if self.state == "eliminated":
            return
        SCREEN.blit(self.image, self.screen_position())

    """
    # ----------- Bot Players ----------

    def bot_turn(self, grid, list_of_players):
        if self.state != "alive":
            return

        #---- Basic Bot Logic ----
        candidates = []
        for d_row, d_file in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            pos = (self.row + d_row, self.file + d_file, self.col)
            cube = grid.cube_dict.get(pos)
            if cube:
                candidates.append(cube)
        if not candidates:
            return

        strongest_cube = candidates[0]
        for cube in candidates:
            if cube.broken_state_number <= strongest_cube.broken_state_number:
                strongest_cube = cube
        movement_coords = (strongest_cube.row - self.row, strongest_cube.file - self.file, strongest_cube.col -self.col)
        #---- ---- ----

        self.move(movement_coords[0], movement_coords[1], movement_coords[2], grid, list_of_players)
        """

    def bot_turn_2(self, grid, list_of_players):
        """
        :param self: type player/cube object
        :param grid: type grid object
        :param list_of_players: list of players
        :return:
        """
        if self.state != "alive":
            return

        dict_of_damage_values = {(coordinates): cube.broken_state_number for coordinates, cube in grid.cube_dict.items()}
        my_position = (self.row, self.file, self.col)
        others_positions = tuple((player.row, player.file, player.col) for player in list_of_players if player is not self)

        move = (0, 0)  # default: stay put
        try:
            result = bots.strongest_closest_square_bot.choose_move(my_position, dict_of_damage_values, others_positions)
            if result in VALID_BOT_MOVES:
                move = result
            else:
                print(f"{self.player_name} returned an invalid move: {result!r}")
        except Exception as error:
            print(f"{self.player_name} crashed: {error!r}")

        d_row, d_file = move
        self.move(d_row, d_file, 0, grid, list_of_players)



