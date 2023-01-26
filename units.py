from errors import *


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    def __init__(self, dot, length, orient_h=True):
        self.dot = dot
        self.length = length
        self.orient_h = orient_h
        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            dot_x = self.dot.x
            dot_y = self.dot.y

            if self.orient_h:
                dot_y += i

            else:
                dot_x += i

            ship_dots.append(Dot(dot_x, dot_y))
        return ship_dots

    def shot_hit(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid

        self.destroyed = 0

        self.board_field = [['o'] * self.size for _ in range(self.size)]

        self.ships = []
        self.occupied = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.occupied:
                raise BoardPlaceShipException()
        for d in ship.dots:
            self.board_field[d.x][d.y] = '■'
            self.occupied.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, offset_visible=False):
        offset = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        for d in ship.dots:
            for dx, dy in offset:
                offset_dot = Dot(d.x + dx, d.y + dy)
                if not(self.out(offset_dot)) and offset_dot not in self.occupied:
                    if offset_visible:
                        self.board_field[offset_dot.x][offset_dot.y] = '.'
                    self.occupied.append(offset_dot)

    def __str__(self):
        output = '  |'
        for i in range(self.size):
            output += f' {i + 1} |'
        for j, row in enumerate(self.board_field):
            output += f'\n{chr(97 + j)} | {" | ".join(row)} |'

        if self.hid:
            output = output.replace('■', 'o')
        return output

    def out(self, dot_to_check):
        return not((0 <= dot_to_check.x < self.size) and (0 <= dot_to_check.y < self.size))

    def shot(self, target):
        if self.out(target):
            raise BoardOutException

        if target in self.occupied:
            raise BoardDoubleShotException

        self.occupied.append(target)

        for ship in self.ships:
            if ship.shot_hit(target):
                ship.lives -= 1
                self.board_field[target.x][target.y] = 'x'
                if not ship.lives:
                    self.destroyed += 1
                    self.contour(ship, offset_visible=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль поврежден!')
                    return True

        self.board_field[target.x][target.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.occupied = []
