from CONSTANTS import *
from Cube import Cube, Player
from Grid import Grid


grid = Grid()
player1 = Player(0, 0, TOP_LAYER, RED_CUBE_IMAGE)
player2 = Player(NUMBER_OF_CUBES-1, NUMBER_OF_CUBES-1, TOP_LAYER, BLUE_CUBE_IMAGE)

list_of_players = [player1, player2]

MOVES = {
    pygame.K_z: (-1, 0, 0, player1),
    pygame.K_s: (1, 0, 0, player1),
    pygame.K_q: (0, -1, 0, player1),
    pygame.K_d: (0, 1, 0, player1),
    pygame.K_UP: (-1, 0, 0, player2),
    pygame.K_DOWN: (1, 0, 0, player2),
    pygame.K_LEFT: (0, -1, 0, player2),
    pygame.K_RIGHT: (0, 1, 0, player2),
    #pygame.K_SPACE: (0, 0, 1),
    #pygame.K_LALT: (0, 0, -1)
}

SCREEN.fill((100, 150, 100))
grid.draw(list_of_players)
pygame.display.flip()
pygame.time.wait(1000)

while True:
    SCREEN.fill((100, 150, 100))
    grid.draw(list_of_players)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key in MOVES:
                d_row,d_file,d_col,player = MOVES[event.key]
                target_position = (player.row + d_row, player.file + d_file, player.col + d_col)
                if target_position in grid.cube_dict:
                    player.row, player.file, player.col = target_position
            if event.key == pygame.K_p:
                grid.cube_dict.pop((player1.row, player1.file, player1.col))
                player1.col -=1

    for player in list_of_players:
        try:
            if grid.cube_dict[player.row, player.file, player.col].transparency <-20:
                    grid.cube_dict.pop((player.row, player.file, player.col))
                    player.col -= 1
            else:
                grid.cube_dict[player.row, player.file, player.col].transparency -= 5
        except:
            print(player.image, "LOSS")
            break

    pygame.display.flip()
    CLOCK.tick(60)


