from random import randint
from CONSTANTS import *
from Cube import Cube
from Grid import Grid

pygame.init()
pygame.display.set_caption(CAPTION)

player_layer = 0

#create_grid(NUMBER_OF_CUBES)
grid = Grid()

coords = [0,0,player_layer+1]
cube1 = Cube(SCREEN.get_width() / 2, (SCREEN.get_height() - TOTAL_GRID_HEIGHT) / 2, CUBE_SIZE * 0.5, 0, 0, player_layer, RED_CUBE_IMAGE)

#falling_cube = Cube(screen.get_width() / 2, (screen.get_height() - TOTAL_GRID_HEIGHT) / 2, 100, randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_CUBES - 1), randint(0, NUMBER_OF_LAYERS), BLUE_CUBE_IMAGE)

while True:
    SCREEN.fill((100, 150, 100))
    grid.draw(coords, cube1)

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
            cube1.x_offset = SCREEN.get_width() / 2
            cube1.y_offset = (SCREEN.get_height() - TOTAL_GRID_HEIGHT) / 2


    pygame.display.flip()
    CLOCK.tick(60)


