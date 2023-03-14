from enum import Enum
from termcolor import colored

# from termcolor_extensions import get_color


MAX_ROW = 6

MAX_COL = 9


def blue2red(position):
    return MAX_ROW - position[0], position[1]


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


BLUE_ROWS = [2, 1, 0]
RED_ROWS = [4, 5, 6]
MID_ROW = 3


class Board:
    n_rows = MAX_ROW + 1
    n_cols = MAX_COL + 1

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
        return [([BlankSquare()] * self.n_cols).copy() for _ in range(self.n_rows)]

    def freeze_divider(self, grid):
        n_cols = self.n_cols
        for i in range(n_cols):
            grid[3][i] = DividerSquare()

    def freeze_players(self, grid):
        for team in [self.red_team, self.blue_team]:
            for player in team.players:
                if isinstance(grid[player.row][player.column], PrisonSquare):
                    prison_square = grid[player.row][player.column]
                    grid[player.row][player.column] = OccupiedPrisonSquare(prison_square.color, player)
                else:
                    grid[player.row][player.column] = player

    def freeze_prisons(self, grid):
        for team in [self.red_team, self.blue_team]:
            team.freeze_prison(grid)

    def freeze_flags(self, grid):
        for team in [self.red_team, self.blue_team]:
            flag = team.flag
            grid[flag.row][flag.column] = flag

    def freeze(self):
        grid = self.draw_blank()
        self.freeze_divider(grid)
        self.freeze_prisons(grid)
        self.freeze_flags(grid)
        self.freeze_players(grid)
        return grid

    def print(self):
        print('╔═══' + '══' * (self.n_cols - 2) + '══╗')
        for row in self.freeze():
            row_strings = [element.draw() for element in row]
            string = ' '.join(row_strings)
            print('║ ' + string + ' ║')
        print('╚═══' + '══' * (self.n_cols - 2) + '══╝')

    def play_game(self, board):
        game_finished = False
        while not game_finished:
            for team in [self.blue_team, self.red_team]:
                self.print()
                current_grid = self.freeze()
                while True:
                    try:
                        player_number, direction = self.get_move(team)
                        player = team.players[player_number]
                        player.move(direction, current_grid)
                        break
                    except InvalidMoveError as err:
                        print(colored('That move is not valid, try again.\n' + str(err), team.color))
                        self.n_invalid_moves += 1
                target_object = self.character_at_position(current_grid, player.position)
                if isinstance(target_object, Player):
                    target_object.send_to_prison(team)
                    player.send_to_prison(target_object.team(board))
                elif isinstance(target_object, Flag):
                    player.pick_up_flag(target_object)
                if (not player.in_prison  # this can happen if player sends themself to prison
                        and ((player.color == 'red' and player.position in BLUE_PRISON)
                             or (player.color == 'blue' and player.position in RED_PRISON))):
                    team.release_all(current_grid)
                if player.holding_flag:
                    if isinstance(target_object, DividerSquare):
                        print(colored(player.color + ' has won this game!!!', player.color))
                        game_finished = True
                        break

    @staticmethod
    def character_at_position(grid, position):
        return grid[position[0]][position[1]]


class Team:

    def __init__(self, color, n_players, starting_positions, prison, flag_position, name):
        self.flag = Flag(flag_position, color)
        self.color = color
        self.prison = prison
        self.players = [Player(i, color, starting_positions[i]) for i in range(n_players)]
        self.gamer_name = name

    def freeze_prison(self, grid):
        for position in self.prison:
            grid[position[0]][position[1]] = PrisonSquare(self.color)

    def release_all(self, grid):
        for player in self.players:
            player.release(grid, self)


class Player:

    def __init__(self, number, color, position):

        self.row = position[0]
        self.column = position[1]
        self.number = number
        self.color = color
        self.holding_flag = None
        self.in_prison = False

    def team(self, board):
        team = board.color2team(self.color)
        return team

    def get_released_position(self, grid, row, col):
        try_col_num = 0
        while not isinstance(grid[row][col], BlankSquare):
            if not col == 9:
                col += 1
            else:
                col = 0
            try_col_num = try_col_num + 1
            if try_col_num == 9:
                if row < 3:
                    if row < 1 or row == 1:
                        row = row + 1
                    if row == 2:
                        row = row - 1
                if row > 3:
                    if row < 5 or row == 5:
                        row = row + 1
                    if row == 6:
                        row = row - 1
        return row, col

    def release(self, grid, team):
        if self.in_prison:
            if self.color == 'red':
                starting_positions = RED_STARTING_POSITIONS
            else:
                starting_positions = BLUE_STARTING_POSITIONS
            row, col = starting_positions[self.number]
            row, col = self.get_released_position(grid, row, col)
            self.row = row
            self.column = col
            self.in_prison = False

    def drop_flag(self):
        self.holding_flag = None

    def pick_up_flag(self, flag):
        self.holding_flag = flag

    @property
    def is_capturable(self):
        if self.row == MID_ROW:
            return False
        if self.color == 'blue' and self.row in BLUE_ROWS:
            return False
        elif self.color == 'red' and self.row in RED_ROWS:
            return False
        else:
            return True

    @property
    def position(self):
        return self.row, self.column

    def move(self, direction, board):
        target_row = self.row
        target_col = self.column
        if not self.in_prison:
            if direction == Direction.UP:
                if self.row == 0:
                    raise InvalidMoveError('That move takes you outside the board')
                target_row -= 1
            elif direction == Direction.DOWN:
                if self.row == 6:
                    raise InvalidMoveError('That move takes you outside the board')
                target_row += 1
            elif direction == Direction.LEFT:
                if self.column == 0:
                    raise InvalidMoveError('That move takes you outside the board')
                target_col -= 1
            elif direction == Direction.RIGHT:
                if self.column == 9:
                    raise InvalidMoveError('That move takes you outside the board')
                target_col += 1
        elif self.in_prison:
            raise InvalidMoveError('Player ' + str(self.number) + ' is in prison')
        target = (target_row, target_col)
        target_object = Board.character_at_position(board, target)
        if isinstance(target_object, PrisonSquare):
            if target_object.color == self.color:
                raise InvalidMoveError('That move would take you onto your prison')
        elif isinstance(target_object, Flag):
            if target_object.color == self.color:
                raise InvalidMoveError('That move would take you onto your flag')
        elif isinstance(target_object, Player):
            if target_object.color == self.color or target_row == 3:
                raise InvalidMoveError('That move would take you onto another player')
        elif isinstance(target_object, OccupiedPrisonSquare):
            raise InvalidMoveError('That move would take you onto another player')
        self.row, self.column = target
        if self.holding_flag is not None:
            self.holding_flag.update_position(target)

    def draw(self):
        if self.in_prison:
            color = 'grey'
        else:
            color = self.color

        # if self.position in RED_PRISON:
        #     on_color = 'on_red'
        # elif self.position in BLUE_PRISON:
        #     on_color = 'on_blue'
        if self.holding_flag is not None:
            on_color = 'on_white'
        else:
            on_color = None
        return colored(str(self.number), color, on_color=on_color)

    def send_to_prison(self, capturing_team):
        if self.is_capturable and self.color != capturing_team.color:
            self.drop_flag()
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


class Flag:
    def __init__(self, position, color):
        self.is_movable_by_team = False
        self.row = position[0]
        self.column = position[1]
        self.color = color

    def update_position(self, new_position):
        self.row = new_position[0]
        self.column = new_position[1]

    def draw(self):
        return colored('#', self.color)

    def detect_win(self):
        position = (self.row, self.column)
        if self.color == 'blue':
            if position in RED_STARTING_POSITIONS:
                red_win = True
                return red_win
        if self.color == 'red':
            if position in BLUE_STARTING_POSITIONS:
                blue_win = True
                return blue_win


class PrisonSquare:
    def __init__(self, color):
        self.color = color

    def draw(self):
        char = ' '
        return colored(char, on_color='on_' + self.color)


class OccupiedPrisonSquare(PrisonSquare):
    def __init__(self, color, occupant):
        super().__init__(color)
        self.occupant = occupant

    def draw(self):
        char = self.occupant.draw()
        return colored(char, on_color='on_' + self.color)



class BlankSquare:

    @staticmethod
    def draw():
        char = ' '
        return char


class DividerSquare:

    @staticmethod
    def draw():
        char = '-'
        return char


def main():
    board = Board()
    board.play_game(board)


if __name__ == '__main__':
    main()
