from random import randint
from units import *
from errors import *
from time import sleep


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        sleep(4)
        dot_shot = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {chr(dot_shot.x + 97)} {dot_shot.y + 1}')
        return dot_shot


class User(Player):
    def ask(self):
        while True:
            coordinates = input('Ваш ход: ').replace(' ', '')

            if len(coordinates) != 2:
                print('Введите 2 координаты!')
                continue

            x, y = coordinates[0].lower(), coordinates[1]

            if not (x.isalpha()) or not (y.isdigit()):
                print('Введите букву и число!')
                continue

            x, y = ord(x) - 97, int(y)
            return Dot(x, y - 1)


class Game:
    def __init__(self, size, ships=6):
        self.size = 6 if size < 5 else size
        self.ships = 8 if ships > 6 and self.size > 7 else 6
        self.lengths_of_ships = {6: [3, 2, 1, 1, 1, 1], 8: [4, 3, 3, 2, 1, 1, 1, 1]}
        player = self.random_board()
        comp = self.random_board()
        comp.hid = True

        self.ai = AI(comp, player)
        self.user = User(player, comp)

    def generate_board(self):
        board = Board(size=self.size)
        attempts = 0
        for length in self.lengths_of_ships[self.ships]:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardPlaceShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while not board:
            board = self.generate_board()
        return board

    def greet(self):
        print('''
---------------------------
|     Приветствуем Вас    |
|         в игре          |
|       МОРСКОЙ БОЙ       |
---------------------------
|     формат ввода: x y   |
|     x - буква строки    |
|     y - номер столбца   |
---------------------------''')

    def boards_refresh(self):
        user_board = self.user.board.__str__().split('\n')
        comp_board = self.ai.board.__str__().split('\n')
        print('-' * (self.size * 5))
        print('Доска пользователя:'.ljust(self.size * 5), 'Доска компьютера:')
        for row_user, row_comp in zip(user_board, comp_board):
            print(str(row_user).ljust(self.size * 5), row_comp)
        print('-' * (self.size * 5))

    def loop(self):
        turn = 0
        while True:
            self.boards_refresh()
            if turn % 2 == 0:
                print('Ходит пользователь!')
                repeat = self.user.move()
            else:
                print('Ходит компьютер!')
                repeat = self.ai.move()
            if repeat:
                turn -= 1

            if self.ai.board.destroyed == len(self.lengths_of_ships):
                self.boards_refresh()
                print('Пользователь выиграл!')
                break

            if self.user.board.destroyed == len(self.lengths_of_ships):
                self.boards_refresh()
                print('Компьютер выиграл!')
                break
            turn += 1

    def start(self):
        self.greet()
        self.loop()
