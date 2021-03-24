from enum import Enum
from termcolor import colored

from termcolor_extensions import get_color


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

RED_FLAG = blue2red(BLUE_FLAG)

BLUE_PRISON = [(0, 9),
               (0, 8),
               (0, 7),
               (1, 9),
               (1, 8),
               (1, 7)
               ]


RED_PRISON = [blue2red(position) for position in BLUE_PRISON]


def clear():
    pass


class Board:
    n_rows = 7
    n_cols = 10

    def __init__(self):
        blue_name = input(colored('-> Blue Player: What is your name?', 'blue'))
        red_name = input(colored('-> Red player: What is your name?', 'red'))

        self.n_invalid_moves = 0
        self.blue_team = Team('blue', 10, BLUE_STARTING_POSITIONS, BLUE_PRISON, BLUE_FLAG, blue_name)
        self.red_team = Team('red', 10, RED_STARTING_POSITIONS, RED_PRISON, RED_FLAG, red_name)

    def color2team(self, color):
        if color == 'red':
            return self.red_team
        elif color == 'blue':
            return self.blue_team
        else:
            raise ValueError

    def get_move(self, team):
        move = input(colored(team.gamer_name + ' it is your turn \n make a move:', team.color))
        try:
            player, direction = move
            player = int(player)
            direction = Direction(direction.lower())
            self.n_invalid_moves = 0
        except ValueError:
            self.n_invalid_moves += 1
            if self.n_invalid_moves == 10:
                print(colored('\n Too many invalid moves. Quiting...', team.color))
                quit()
            print(colored('That move is not valid, try again.', team.color))
            return self.get_move(team)
        return player, direction

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

    def play_game(self):
        while True:
            for team in [self.blue_team, self.red_team]:
                self.print()
                current_grid = self.draw()
                while True:
                    try:
                        player_number, direction = self.get_move(team)
                        player = team.players[player_number]
                        player.move(direction, current_grid)
                        break
                    except InvalidMoveError as err:
                        print(colored('That move is not valid, try again.\n' + str(err), team.color))
                        self.n_invalid_moves += 1

                target_square, target_color = self.character_at_position(current_grid, player.position)
                try:
                    target_player = int(target_square)
                except ValueError:
                    target_player = -1
                if target_player >= 0:
                    target_team = self.color2team(target_color)
                    target_player = target_team.players[target_player]
                    target_player.send_to_prison(team)

    @staticmethod
    def character_at_position(grid, position):
        string = grid[position[0]][position[1]]
        try:
            return get_color(string)
        except ValueError:
            return string, None


class Team:

    def __init__(self, color, n_players, starting_positions, prison, flag, name):
        self.flag = flag
        self.color = color
        self.prison = prison
        self.players = [Player(i, color, starting_positions[i]) for i in range(n_players)]
        self.gamer_name = name

    def draw_prison(self, grid):
        for position in self.prison:
            grid[position[0]][position[1]] = colored(grid[position[0]][position[1]], on_color='on_' + self.color)

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
        self.in_prison = False

    @property
    def position(self):
        return self.row, self.column

    def move(self, direction, board):
        if not self.in_prison:
            if direction == Direction.UP:
                if self.row == 0:
                    raise InvalidMoveError('That move takes you outside the board')
                self.row -= 1
            elif direction == Direction.DOWN:
                if self.row == 6:
                    raise InvalidMoveError('That move takes you outside the board')
                self.row += 1
            elif direction == Direction.LEFT:
                if self.column == 0:
                    raise InvalidMoveError('That move takes you outside the board')
                self.column -= 1
            elif direction == Direction.RIGHT:
                if self.column == 9:
                    raise InvalidMoveError('That move takes you outside the board')
                self.column += 1
        elif self.in_prison:
            raise InvalidMoveError('Player ' + str(self.number) + ' is in prison')

    def draw(self, board):
        if self.in_prison:
            color = 'grey'
        else:
            color = self.color
        board[self.row][self.column] = colored(str(self.number), color)

    def send_to_prison(self, capturing_team):
        position = capturing_team.prison[0]
        self.row = position[0]
        self.column = position[1]
        self.in_prison = True


class Direction(Enum):
    UP = 'u'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'


class InvalidMoveError(Exception):
    pass


class Gamer:
    pass


def main():
    board = Board()
    board.play_game()


if __name__ == '__main__':
    main()
