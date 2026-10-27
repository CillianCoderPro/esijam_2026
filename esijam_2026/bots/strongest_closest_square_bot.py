def choose_move(my_position, dict_of_damage_values, others_positions):
    """
    :param my_position: (row, file, col) of your cube
    :param dict_of_damage_values: {(row, file, col): damage} ---- 0 = intact, higher = closer to breaking ---- A cube missing from the dict is gone.
    :param others_positions: tuple of (row, file, col), one per opponent still in the game
    :return: (d_row, d_file): (0, 0) stay, (-1, 0)/(1, 0): row --- (0, -1)/(0, 1): file
    Anything else (a crash) makes you stay put.
    """

    legal_moves = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))
    row, file, col = my_position

    best_move = (0, 0)
    best_damage = None
    for d_row, d_file in legal_moves:
        possible_position = (row + d_row, file + d_file, col)
        damage = dict_of_damage_values.get(possible_position)
        if damage is None or possible_position in others_positions:     # no cube to stand on or someone is standing on it
            continue                                                    # continur to the next loop itieration
        if best_damage is None or damage <= best_damage:                # on ties, the last direction wins
            best_move = (d_row, d_file)
            best_damage = damage
    return best_move