from enum import Enum
from string import ascii_uppercase
from termcolor import colored

# N_COLS = 10
# N_ROWS = 7


def clear():
    pass


def l():
    return ''' '''


def printBoard():
    clear()
    header = ascii_uppercase[0:N_COLS]
    print('     ' + '   '.join(header))
    print('   ╔══' + '═╦══' * (N_COLS - 1) + '═╗')
    for r in range(0, N_ROWS):
        entries = [str(l()) for _ in (range(N_COLS))]
        if r < 10:
            spacing = ' '
        else:
            spacing = ''
        print(spacing + str(r), '║', ' ║ '.join(entries), '║')
        if not r == N_ROWS - 1:
            print('   ╠══' + '═╬══' * (N_COLS - 1) + '═╣')
    print('   ╚══' + '═╩══' * (N_COLS - 1) + '═╝')


class Board:
    n_rows = 7
    n_cols = 10

    def __init__(self):
        self.red_team = Team('red', 10)
        self.blue_team = Team('blue', 10)

    def print(self):
        printable = [([' '] * self.n_cols).copy() for _ in range(self.n_rows)]
        for team in [self.red_team, self.blue_team]:
            for player in team.players:
                player.print(printable)
        for row in printable:
            string = ' '.join(row)
            print(string)


class Team:
    def __init__(self, color, n_players):
        self.color = color
        if color == 'red':
            row = 1
        else:
            row = 0
        self.players = [Player(i, color, row, i) for i in range(n_players)]


class Player:
    def __init__(self, number, color, row, column):
        self.row = row
        self.column = column
        self.number = number
        self.color = color

    def move(self, direction):
        pass

    def print(self, board):
        # row = list(board[self.row])
        board[self.row][self.column] = colored(str(self.number), self.color)
        # board[self.row] = ''.join(row)


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Gamer:
    pass


def main():
    # player_1 = input('-> What is your name player 1')
    # player_2 = input('-> what is your name player 2')
    # printBoard()
    board = Board()
    board.print()


if __name__ == '__main__':
    main()