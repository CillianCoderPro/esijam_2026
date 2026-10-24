from pygame import K_SPACE, K_PRINT

from CONSTANTS import *
from Cube import Cube
from Grid import Grid


grid = Grid()
player = Cube(NUMBER_OF_CUBES//2,NUMBER_OF_CUBES//2,TOP_LAYER, RED_CUBE_IMAGE, 255)
player.z = CUBE_SIZE * 0.5
SCREEN.fill((100, 150, 100))
grid.draw(player)

while True:
    SCREEN.fill((100, 150, 100))
    grid.draw(player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key in MOVES:
                d_row,d_file,d_col = MOVES[event.key]
                target_position = (player.row + d_row, player.file + d_file, player.col + d_col)
                if target_position in grid.cube_dict:
                    player.row, player.file, player.col = target_position
            if event.key == pygame.K_p:
                grid.cube_dict.pop((player.row, player.file, player.col))
                player.col -=1

    grid.cube_dict[player.row, player.file, player.col].transparency -=5
    if grid.cube_dict[player.row, player.file, player.col].transparency <-20:
        grid.cube_dict.pop((player.row, player.file, player.col))
        player.col -= 1

    pygame.display.flip()
    CLOCK.tick(60)


