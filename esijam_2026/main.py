from CONSTANTS import *
from Cube import Cube, Player
from Grid import Grid


grid = Grid()

list_of_players = []

for i in range(NUMBER_OF_PLAYERS):
    row, file = PLAYER_CONFIGURATIONS[i]["start"]
    image = PLAYER_CONFIGURATIONS[i]["image"]
    player = Player(row, file, TOP_LAYER, image)
    list_of_players.append(player)


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
            for i, player in enumerate(list_of_players):
                if event.key in PLAYER_CONFIGURATIONS[i]["moves"]:
                    d_row,d_file,d_col = PLAYER_CONFIGURATIONS[i]["moves"][event.key]
                    player.move(d_row, d_file, d_col, grid)


    for player in list_of_players:
        try:
            if grid.cube_dict[player.row, player.file, player.col].transparency <-100:
                    grid.cube_dict.pop((player.row, player.file, player.col))
                    player.col -= 1
            else:
                grid.cube_dict[player.row, player.file, player.col].transparency -= 5
        except:
            player.state = "eliminated"

    pygame.display.flip()
    CLOCK.tick(60)


