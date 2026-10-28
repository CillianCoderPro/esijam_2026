from CONSTANTS import NUMBER_OF_GRID_CUBE_IMAGES


def choose_move(my_position, dict_of_damage_values, others_positions):
    """
    :param my_position: (row, file, col) of your cube
    :param dict_of_damage_values: {(row, file, col): damage} ---- 0 = intact, higher = 4 = closer to breaking ---- A cube missing from the dict is gone.
    :param others_positions: tuple of (row, file, col), one per opponent still in the game
    :return: (d_row, d_file): (0, 0) stay, (-1, 0)/(1, 0): row --- (0, -1)/(0, 1): file
    Anything else (a crash) makes you stay put.
    """
    LEGAL_MOVES = ((-1, 0), (1,0), (0, -1), (0, 1), (0, 0))
    MY_ROW, MY_FILE, MY_COL = my_position
    BLOCKED_SQUARES = others_positions
    INF = float("inf")
    DEPTH = 4


    def best(row, file, depth):
        best_move = (0, 0)
        best_score = INF

        for d_row, d_file in LEGAL_MOVES:
            new_row , new_file = row + d_row , file + d_file
            square = (new_row, new_file, MY_COL)
            damage = dict_of_damage_values.get(square)
            if damage is None or square in BLOCKED_SQUARES or damage == 4:
                continue
            elif depth == 0:
                score = damage
            else:
                _, score = best(new_row, new_file, depth-1)
                score += damage
            if score < best_score:
                best_move , best_score = (d_row, d_file), score
        return best_move, best_score

    move, _ = best(MY_ROW, MY_FILE, DEPTH)
    print(move)

    return move