from random import choice

def choose_move(my_position, dict_of_damage_values, others_positions):
    """
    :param my_position: tuple of my coordinates
    :param dict_of_damage_values: dictionary of all cubes in the grid: dict_of_damage_values[row, file, col] = cube
    :param others_positions: list of tuple of coordinates of other players
    :return: coordinates in the form: (0,0) --> "stay put" ; (1,0) --> "go down"
    """
    """
    print(my_position)
    print(others_positions)
    print(dict_of_damage_values)
    """

    legal_moves = ((0, 0), (-1, 0), (1,0), (0, -1), (0, 1))
    return choice(legal_moves)