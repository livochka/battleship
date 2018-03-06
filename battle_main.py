# The module created to represent BattleShip game with OOP

from battle import change, has_ship, find_foreign, is_valid, ship_size, \
    field_to_str
from copy import deepcopy
from random import randrange


class Ship:
    """
    Class for representing ships
    """

    def __init__(self, lenght, cells, horisontal=True, bow=(0, 0)):
        self.bow = bow
        self.horisontal = horisontal
        self.__length = lenght
        self.cell = cells
        self.__hit = []

    def shoot_at(self, part):
        """
        Do shooting
        part: part you will shoot
        """
        self.__hit.append(part)

    def delete_ship(self):
        """
        Deleting ship, if list of shoot sides is equal to all ship sides
        """
        if len(self.__hit) == self.__length:
            points = self.cell
            return points, self
        return False


class Field:
    """
    Class for representing fields for BattleShip game
    """

    def __init__(self):
        self.__ships = []
        self.field = self.generate_field()
        self.destroyed = 0

    def _find_ship_for_position(self, position):
        """
        tuple -> Ship
        position: position with part of the ship
        return: all ship
        """
        for ship in self.__ships:
            if position in ship.cell:
                return ship

    def _find_ship(self, bow):
        """
        If ship with such bow exist - returns True
        bow: bow of the ship
        """
        for ship in self.__ships:
            if ship.bow == bow:
                return True

    def _add_ships(self, field):
        """
        Adds ships (Ship) to the field
        field: BattleShip game field
        """
        for row in range(10):
            for point in range(10):
                if field[row][point] == '*':
                    ship = ship_size((chr(point + 65), row + 1), field)
                    bow = min(ship[1])
                    if not self._find_ship(bow):
                        try:
                            horizontal = True if ship[1][0] == ship[1][1] \
                                else False
                        except IndexError:
                            horizontal = True
                        self.__ships.append(Ship(len(ship[1]), ship[1],
                                               horizontal, bow))

    def _generate_ships(ships, rows, columns, directions, field):
        """
        Generates ships on the field
        ships: dictionary with all ships and sizes
        rows: numbers of rows on field
        columns: numbers of columns on field
        directions: available directions (left, right, up, down)
        field: game field
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
                                        find_foreign(change(coord),
                                                     (4, coordinates), field):
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

    _generate_ships = staticmethod(_generate_ships)

    def mark_cell(self, point, mark):
        """
        Make specified mark on the game field
        point: coordinates of the point
        mark: type of mark
        """
        self.field[point[1] - 1][ord(point[0]) - 65] = mark

    def shoot_at(self, point):
        """
        Allows to shoot Ship
        point: coordinates of shoot point
        """
        print(point)
        if self.field[point[1] - 1][ord(point[0]) - 65] == '*':
            ship = self._find_ship_for_position(point)
            ship.shoot_at(point)
            points = ship.delete_ship()
            self.mark_cell(point, '+')


            # If ship is dead
            if points:
                for i in points[0]:
                    self.mark_cell(i, 'Y')

                # removing ship from field ships list
                self.__ships.remove(points[1])
                self.destroyed += 1
        else:
            self.mark_cell(point, 'X')

    def field_without_ships(self):
        """
        Shows field without ships
        """
        field = field_to_str(self.field).replace('*', '-')
        return field

    def field_with_ships(self):
        """
        Shows field with ships
        """
        return field_to_str(self.field)

    def generate_field(self):
        """
        Created to generate game field
        """
        ships = {4: 1, 3: 2, 2: 3, 1: 4}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        rows = [x for x in range(0, 10)]
        columns = [x for x in range(0, 10)]
        # Creating of empty field
        field = [['-'] * 10 for i in range(10)]
        field1 = self._generate_ships(ships, rows, columns, directions,
                                      deepcopy(field))
        while not is_valid(field1[0]):
            field1 = self._generate_ships(ships, rows, columns, directions,
                                          deepcopy(field))

        field = field1[0]
        # Adding ships
        self._add_ships(field)
        return field


class Player:
    """
    Created to represent Player
    """

    def __init__(self, name, field):
        self.name = name
        self.field = field


class Game:
    """
    Represents BattleShip Game
    """

    def __init__(self):
        players = self._intro()
        self.fields = [Field(), Field()]
        self.players = [Player(players[0], self.fields[0]),
                        Player(players[1], self.fields[1])]
        self.run()

    def _intro():
        """
        Intro of the game, asks for players names
        return: (name1, name2)
        """
        print("Hey, this is a BattleShip Game!")
        print("If you heat the ship cell look like '*', if you destroy "
              "ship it looks like 'YYY'. If you did not get it, just 'X'")
        player1 = input("Player 1, enter your name, please: ")
        player2 = input("Player 2, enter your name, please: ")
        return player1, player2

    _intro = staticmethod(_intro)

    def read_position(player):
        """
        Allows to read position from user
        return: coordinates of the position
        """
        while True:
            answer = input("Player {}, enter move: ".format(player.name))
            print(answer[1::])
            if len(answer) in (2, 3) and 64 < ord(answer[0]) < 75 \
                    and 0 < int(answer[1::]) < 11:
                return answer[0], int(answer[1::])

    read_position = staticmethod(read_position)

    def run(self):
        """
        Run the BattleShip game
        """
        while True:
            print("Player 1, your turn! Good luck!")
            print(self.fields[1].field_without_ships())
            position = self.read_position(self.players[0])
            self.fields[1].shoot_at(position)
            if self.fields[0].destroyed == 10:
                print("Player 1, you win!")
            print("Player 2, your turn! Good luck!")
            print(self.fields[0].field_without_ships())
            position = self.read_position(self.players[1])
            self.fields[0].shoot_at(position)
            if self.fields[1].destroyed == 10:
                print("Player 2, you win!")


if __name__ == '__main__':
    g = Game()
