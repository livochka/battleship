from random import randrange
from copy import deepcopy


def read_file(filename):
    """
    (str) -> list
    filename: path to file
    return: list with ships and '-' if no ship here
    """
    with open(filename, encoding='utf-8') as f:
        coordinates = []
        info = f.readlines()[0:10]
        for line in info:
            coordinates.append(list(line[0:10]))
    return coordinates


def has_ship(coord, field):
    """
    (tuple, list) -> bool
    Checking is there a ship
    coord: tuple with coordinates of the ceil
    return: True if ceil has a ship, else False
    """
    row, column = int(coord[1]) - 1, ord(coord[0]) - 65
    if field[row][column] == '*':
        return True
    return False


def check_row(row, row_num, start, end, step, reverse=False):
    """
    (list, int, int, int, int, bool) -> (int, list)
    Created to find ship in row
    row: row with ships (or without)
    row_num: number of this row in field
    start: we start looking from this position
    end: actually end of the row
    step: mean direction - left or right
    reverse: if we looking up or down we need to reverse row and column after
    return: size of the ship in this direction and coordinates
    """
    number = 1
    coordinates = [[start, row_num]]
    for move in range(start + step, end, step):
        if row[move] == '*':
            number += 1
            coordinates.append([move, row_num])
        else:
            break

    # If up or down direction
    if reverse:
        for x in coordinates:
            x.reverse()

    coordinates = list(change(x) for x in coordinates)
    return number, coordinates


def find_foreign(point, ship, field):
    """
    We looking for all close to the point parts of ships
    (tuple, tuple, list) -> bool
    point: our point
    ship: point is a part of the ship
    field: whole field on which we are looking for foreigns
    return: False, if point has foreign neighbours (which are not parts of
    parameter ship), else - True
    """

    # Allowed neighbours are parts of the ship
    allowed = ship[1]

    row, column = int(point[1]) - 1, ord(point[0]) - 65

    # All neighbours directions
    directions = [(-1, 0), (0, 1), (0, -1), (1, 0), \
                  (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for i in directions:
        if 0 < column + i[0] < 10 and 0 < row + i[1] < 10:
            diagonal = change((column + i[0], row + i[1]))
            if has_ship(diagonal, field) and diagonal not in allowed:
                return True
    return False


def ship_size(coord, field):
    """
    (tuple, list) -> list of False
    coord: coordinates of the point on the field
    field: BattleShip field
    return: tuple with the size of ship and coordinates, if it is not
    ship - False
    """
    # r for rows, c for columns
    if not has_ship(coord, field):
        return 0
    r, c = int(coord[1]) - 1, ord(coord[0]) - 65

    # Looking in all directions
    left = check_row(field[r], r, c, -1, -1)
    right = check_row(field[r], r, c, 10, 1)

    # reversing for up and down, creating of vertical row
    column = list(field[x][c] for x in range(len(field)))
    down = check_row(column, c, r, 10, 1, reverse=True)
    up = check_row(column, c, r, 0, -1, reverse=True)

    directions = [[(left[0] + right[0] - 1), list(set(left[1] + right[1]))],
                  [(up[0] + down[0] - 1), list(set(up[1] + down[1]))]]
    ship = max(directions)
    for point in ship[1]:
        if find_foreign(point, ship, field):
            return False
    # if left[0] + right[0] + up[0] + down[0] == ship[0] + 3:
    return ship


def change(coor):
    """
    tuple -> tuple
    Change coordinates from ('A', 1) type to (0, 0) type
    """
    return chr(coor[0] + 65), coor[1] + 1


def is_valid(field):
    """
    list -> bool
    Checks whether field is valid
    field: field with ships
    return: True, if it can be game field, else - False
    """
    requirement = {4: 1, 3: 2, 2: 3, 1: 4}
    ships = {4: 0, 3: 0, 2: 0, 1: 0}
    used = []
    for row in range(len(field)):
        for column in range(len(field[row])):
            if row < 10 or column < 10:
                coord = change((column, row))
                ship = has_ship(coord, field)
                if ship:
                    ship = ship_size(coord, field)
                    if ship and ship[0] > 0 and ship[1][0] not in used:
                        try:
                            ships[ship[0]] += 1
                            used.extend(ship[1])
                        except KeyError:
                            return False
            else:
                return False
    return requirement == ships


def generate_ships(ships, columns, rows, directions, field):
    """
    (dictionary, list, list, list, list) -> list, dictionary
    ships: dictionary with key for size of ships and value for number of
    ships with that size
    columns: list with markers for columns
    rows: list with markers for rows
    directions: list with available directions
    field: clear game field
    return: game field with ships
    """
    ships2 = {4: [], 3: [], 2: [], 1: []}
    for x in ships:
        # Begins with ship with size 4
        number = ships[x]
        for i in range(number):
            while True:

                # Random start and random direction
                start = (columns[randrange(10)], rows[randrange(10)])
                coord = change(start)
                if not has_ship(coord, field):
                    direction = directions[randrange(4)]
                    coordinates = [coord]

                    try:
                        # Try to create ship in specified direction
                        for k in range(1, x):
                            coord = (start[0] + direction[0] * k, \
                                     start[1] + direction[1] * k)
                            if has_ship(change(coord), field) or \
                                    find_foreign(change(coord), (4,
                                                                 coordinates),
                                                 field):
                                break
                            coordinates.append(change(coord))

                        # If we put on field ship with needed size, we add
                        # its coordinates to all coordinates and mark it on
                        # the field
                        if len(coordinates) == x:
                            for point in coordinates:
                                r, c = point[1] - 1, ord(point[0]) - 65
                                field[r][c] = '*'
                            ships2[x].append(coordinates)
                            break
                    except IndexError:
                        continue
    return field, ships2


def field_to_str(field):
    """
    (list) -> str
    Converts field to string
    field: game field
    """
    my_field = '   A B C D E F G H I J\n'
    for i in range(len(field)):
        if i == 9:
            line = str(i + 1) + ' ' + ' '.join(field[i]) + '\n'
        else:
            line = str(i + 1) + '  ' + ' '.join(field[i]) + '\n'
        my_field += line
    return my_field


def generate_field():
    """
    Generates game field
    return: game field
    """
    ships = {4: 1, 3: 2, 2: 3, 1: 4}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    rows = [x for x in range(0, 10)]
    columns = [x for x in range(0, 10)]

    # Creation of field
    field = [['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
             ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

    field1 = generate_ships(ships, columns, rows, directions, deepcopy(
        field))
    while not is_valid(field1[0]):
        field1 = generate_ships(ships, columns, rows, directions, deepcopy(
            field))

    return field1[0]


if __name__ == '__main__':
    field = generate_field()
    print(field_to_str(field))
