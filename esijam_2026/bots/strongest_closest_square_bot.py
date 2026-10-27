def choose_move(my_position, dict_of_damage_values, others_positions):
    """
    :param my_position: tuple of my coordinates
    :param dict_of_damage_values: dictionary of all cubes in the grid: dict_of_damage_values[row, file, col] = cube
    :param others_positions: list of tuple of coordinates of other players
    :return: coordinates in the form: (0,0) --> "stay put" ; (1,0) --> "go down"
    """

    legal_moves = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))
    row, file, col = my_position

    best_move = (0, 0)
    best_damage = None
    for d_row, d_file in legal_moves:
        position = (row + d_row, file + d_file, col)
        damage = dict_of_damage_values.get(position)
        if damage is None or position in others_positions:  # no cube there, or someone is standing on it
            continue
        if best_damage is None or damage <= best_damage:  # on ties, the last direction wins
            best_move = (d_row, d_file)
            best_damage = damage
    return best_move