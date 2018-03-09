# The module created to represent BattleShip game with OOP


from battle_functions import change, has_ship, find_foreign, is_valid, \
    ship_size, \
    field_to_str
from copy import deepcopy
from random import randrange
from sys import exit


class Ship:
    """
    Class for representing ships
    """
    def __init__(self, bow, length, parts):
        self.bow = bow
        self.__length = length
        self.parts = parts
        self.__hit = []

    def delete_ship(self):
        """
        Allows to know whether ship is destroyed
        return: parts of the ship if destroyed, else - False
        """
        if len(self.__hit) == self.__length:
            return self.parts
        return False

    def shoot_at(self, point):
        """
        Appends shoot part to self.__hit
        point: shoot part
        return: calls self.delete_ship() to check whether ship has already
        destroyed
        """
        self.__hit.append(point)
        return self.delete_ship()


class Field:
    """
    Class for representing game field
    """
    def __init__(self):
        self.ships = []
        self.field = self.correct_ships()

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

    def _find_ship_for_position(self, position):
        """
        Finds ship for its part
        position: coordinates of the part
        return: ship
        """
        for ship in self.ships:
            if position in ship.parts:
                return ship

    def mark_cell(self, point, mark):
        """
        Make specified mark on the game field
        point: coordinates of the point
        mark: type of mark
        """
        self.field[point[1] - 1][ord(point[0]) - 65] = mark

    def shoot_at(self, point, player):
        """
        Makes shoot
        point: point we get on
        player: player who was shoot
        return: True, if shoot was successful
        """
        if self.field[point[1] - 1][ord(point[0]) - 65] == '*':
            ship = self._find_ship_for_position(point)
            self.mark_cell(point, '+')
            directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, 1),
                          (-1, -1), (1, -1)]
            parts = ship.shoot_at(point)
            if parts:
                for i in parts:
                    self.mark_cell(i, 'Y')
                    for x in directions:
                        try:
                            coord = (chr(ord(i[0]) + x[0]), i[1] +
                                     x[1])
                            if not 0 <= ord(coord[0]) - 65 < 10 \
                                    or not 0 < coord[1] <= 10:
                                raise IndexError
                            if coord not in ship.parts:
                                self.mark_cell(coord, 'X')
                        except IndexError:
                            continue
                self.ships.remove(ship)
                player.ships -= 1
            return True
        else:
            self.mark_cell(point, 'X')

    def _find_ship(self, bow):
        """
        If ship with such bow exist - returns True
        bow: bow of the ship
        """
        for ship in self.ships:
            if ship.bow == bow:
                return True

    def _add_ships(self, field):
        """
        Adds objects Ship to the Field
        field: object Field
        """
        for row in range(10):
            for point in range(10):
                if field[row][point] == '*':
                    ship = ship_size((chr(point + 65), row + 1), field)
                    bow = min(ship[1])
                    if not self._find_ship(bow):
                        self.ships.append(Ship(bow, ship[0], ship[1]))

    def _generate_ships(ships, rows, columns, directions, field):
        """
        Generates ships on the field
        ships: dictionary with all ships and sizes
        rows: numbers of rows on field
        columns: numbers of columns on field
        directions: available directions (left, right, up, down)
        field: game field
        """
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
                                break
                        except IndexError:
                            continue
        return field

    _generate_ships = staticmethod(_generate_ships)

    def correct_ships(self):
        """
        Makes ships placement correct
        """
        # Adding ships
        field = self.generate_field()
        self._add_ships(field)
        while True:
            for i in range(20):
                self.ships = []
                self._add_ships(field)
                if len(self.ships) == 10:
                    return field
            field = self.generate_field()

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
        while not is_valid(field1):
            field1 = self._generate_ships(ships, rows, columns, directions,
                                          deepcopy(field))

        field = field1
        return field


class Player:
    """
    Class for representing field
    """
    def __init__(self, name):
        self.name = name
        self.own = Field()
        self.ships = 10


class Game:
    """
    Represents BattleShip Game
    """
    def __init__(self):
        players = self._intro()
        self.player1, self.player2 = Player(players[0]), Player(players[1])

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
            try:
                answer = input("Player {}, enter move: ".format(player.name))
                if len(answer) in (2, 3) and 64 < ord(answer[0]) < 75 \
                        and 0 < int(answer[1::]) < 11:
                    return answer[0], int(answer[1::])
            except Exception:
                continue

    read_position = staticmethod(read_position)

    def player_turn(self, player, opponent):
        """
        Run players turn
        player: player who make shoot
        opponent: players opponent
        return: True, if shoot was successful
        """
        print("Player {}, your turn!".format(player.name))
        print("Your field: \n")
        print(player.own.field_with_ships(), '\n')
        print('Opponent field: \n')
        print(opponent.own.field_without_ships())
        position = self.read_position(player)
        shooting = opponent.own.shoot_at(position, opponent)
        if opponent.ships == 0:
            print("Player {}, you win!".format(player.name))
            exit()
        return shooting

    def run(self):
        """
        Main function, run whole game, make players turn
        """
        while True:
            shooting = self.player_turn(self.player1, self.player2)
            while shooting:
                shooting = self.player_turn(self.player1, self.player2)
            shooting = self.player_turn(self.player2, self.player1)
            while shooting:
                shooting = self.player_turn(self.player2, self.player1)


if __name__ == '__main__':
    m = Game()
    m.run()

