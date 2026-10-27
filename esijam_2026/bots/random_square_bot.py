from random import choice

def choose_move(my_position, dict_of_damage_values, others_positions):
    """
    :param my_position: (row, file, col) of your cube
    :param dict_of_damage_values: {(row, file, col): damage} ---- 0 = intact, higher = closer to breaking ---- A cube missing from the dict is gone.
    :param others_positions: tuple of (row, file, col), one per opponent still in the game
    :return: (d_row, d_file): (0, 0) stay, (-1, 0)/(1, 0): row --- (0, -1)/(0, 1): file
    Anything else (a crash) makes you stay put.
    """

    legal_moves = ((0, 0), (-1, 0), (1,0), (0, -1), (0, 1))
    return choice(legal_moves)