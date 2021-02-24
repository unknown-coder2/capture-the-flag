from enum import Enum
# from string import ascii_uppercase
from termcolor import colored


def blue2red(position):
    max_row = 6
    return max_row - position[0], position[1]


BLUE_STARTING_POSITIONS = [(2, 1),
                           (2, 3),
                           (2, 5),
                           (2, 7),
                           (2, 9),
                           (1, 2),
                           (1, 4),
                           (1, 6),
                           (0, 3),
                           (0, 5)
                           ]

RED_STARTING_POSITIONS = [blue2red(position) for position in BLUE_STARTING_POSITIONS]

BLUE_FLAG = (0, 4)


BLUE_PRISON = [(0, 9),
               (0, 8),
               (0, 7),
               (1, 9),
               (1, 8),
               (1, 7)
               ]


RED_PRISON = [blue2red(position) for position in BLUE_PRISON]


RED_FLAG = blue2red(BLUE_FLAG)


def clear():
    pass


class Board:
    n_rows = 7
    n_cols = 10

    def __init__(self):
        self.red_team = Team('red', 10, RED_STARTING_POSITIONS, RED_PRISON, RED_FLAG)
        self.blue_team = Team('blue', 10, BLUE_STARTING_POSITIONS, BLUE_PRISON, BLUE_FLAG)

    def draw_blank(self):
        return [([' '] * self.n_cols).copy() for _ in range(self.n_rows)]

    def add_divider(self, grid):
        grid[3] = ['-'] * self.n_cols

    def draw_players(self, grid):
        for team in [self.red_team, self.blue_team]:
            for player in team.players:
                player.draw(grid)

    def draw_prisons(self, grid):
        for team in [self.red_team, self.blue_team]:
            team.draw_prison(grid)

    def draw_flags(self, grid):
        for team in [self.red_team, self.blue_team]:
            team.draw_flag(grid)

    def draw(self):
        grid = self.draw_blank()
        self.add_divider(grid)
        self.draw_players(grid)
        self.draw_prisons(grid)
        self.draw_flags(grid)
        return grid

    def print(self):
        print('╔═══' + '══' * (self.n_cols - 2) + '══╗')
        for row in self.draw():
            string = ' '.join(row)
            print('║ ' + string + ' ║')
        print('╚═══' + '══' * (self.n_cols - 2) + '══╝')


class Team:
    def __init__(self, color, n_players, starting_positions, prison, flag):
        self.flag = flag
        self.color = color
        self.prison = prison
        self.players = [Player(i, color, starting_positions[i]) for i in range(n_players)]

    def draw_prison(self, grid):
        for position in self.prison:
            grid[position[0]][position[1]] = colored(grid[position[0]][position[0]], on_color='on_' + self.color)

    def draw_flag(self, grid):
        position = self.flag
        if not grid[position[0]][position[1]] == self.players:
            grid[position[0]][position[1]] = colored('#', self.color)


class Player:
    def __init__(self, number, color, position):
        self.row = position[0]
        self.column = position[1]
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

    def draw(self, board):
        board[self.row][self.column] = colored(str(self.number), self.color)


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
    # else:
        # go(gamer_1, gamer_2, move)


def main():
    # gamer_1 = input('-> What is your name player 1')
    # gamer_2 = input('-> what is your name player 2')
    board = Board()
    board.print()


# def go(gamer_1, gamer_2, move):
#     go_decider = gamer_1
#     if go_decider == gamer_1:
#         go_decider = gamer_2
#     elif go_decider == gamer_2:
#         go_decider = gamer_1
#     else:
#         return go(gamer_1, gamer_2, move)


if __name__ == '__main__':
    main()
