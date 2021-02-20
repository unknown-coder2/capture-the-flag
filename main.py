from enum import Enum
# from string import ascii_uppercase
from termcolor import colored

# N_COLS = 10
# N_ROWS = 7


def clear():
    pass


def space():
    return ''' '''


# def print_board():
#     clear()
#     header = ascii_uppercase[0:N_COLS]
#     print('     ' + '   '.join(header))
#     print('   ╔══' + '═╦══' * (N_COLS - 1) + '═╗')
#     for r in range(0, N_ROWS):
#         entries = [str(space()) for _ in (range(N_COLS))]
#         if r < 10:
#             spacing = ' '
#         else:
#             spacing = ''
#         print(spacing + str(r), '║', ' ║ '.join(entries), '║')
#         if not r == N_ROWS - 1:
#             print('   ╠══' + '═╬══' * (N_COLS - 1) + '═╣')
#     print('   ╚══' + '═╩══' * (N_COLS - 1) + '═╝')


class Board:
    n_rows = 7
    n_cols = 10

    def __init__(self):
        self.red_team = Team('red', 10)
        self.blue_team = Team('blue', 10)

    def print(self):
        printable = [([' '] * self.n_cols).copy() for _ in range(self.n_rows)]
        printable[3] = ['-'] * self.n_cols
        for team in [self.red_team, self.blue_team]:
            for player in team.players:
                player.print(printable)
        print('╔═══' + '══' * (self.n_cols - 2) + '══╗')
        for row in printable:
            string = ' '.join(row)
            print('║ ' + string + ' ║')
        print('╚═══' + '══' * (self.n_cols - 2) + '══╝')


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
        if direction == Direction.UP:
            self.row -= 1
        elif direction == Direction.DOWN:
            self.row += 1
        elif direction == Direction.LEFT:
            self.column -= 1
        elif direction == Direction.RIGHT:
            self.column += 1

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


def get_move(gamer, gamer_1, gamer_2):
    invalid = False
    n = ['']
    c = ['']
    move_1 = move_2 = -1
    if gamer == 'gamer_1':
        move_1 = input(gamer + ' it is your turn \n make a move:')
    elif gamer == 'gamer_2':
        move_2 = input(gamer + ' it is your turn \n make a move:')
    move = move_2 or move_1
    if not move < 2 or move > 2:
        invalid = True
    elif not move[1] == n:
        invalid = True
    elif not move[0] == c:
        invalid = True
    if invalid:
        get_move(gamer, gamer_1, gamer_2)
    else:
        go(gamer_1, gamer_2, move)


def main():
    gamer_1 = input('-> What is your name player 1')
    gamer_2 = input('-> what is your name player 2')
    board = Board()
    board.print()


def go(gamer_1, gamer_2, move):
    go_decider = gamer_1
    if go_decider == gamer_1:
        go_decider = gamer_2
    elif go_decider == gamer_2:
        go_decider = gamer_1
    else:
        return go(gamer_1, gamer_2, move)


if __name__ == '__main__':
    main()
