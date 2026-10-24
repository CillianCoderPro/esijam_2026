from random import randint
from CONSTANTS import *
from Cube import Cube
from Grid import Grid

pygame.init()
pygame.display.set_caption(CAPTION)

grid = Grid()

player = Cube(0,0,0, RED_CUBE_IMAGE)
player.z = CUBE_SIZE * 0.5


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



    pygame.display.flip()
    CLOCK.tick(60)


