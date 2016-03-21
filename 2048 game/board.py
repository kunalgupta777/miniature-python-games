import itertools
import random
from moves import all_moves

board_size = 4
all_tiles = list(itertools.product(range(board_size), range(board_size)))
possible_new_tiles = [4] + ([2] * 9)

#checks for a move that doesn't do anything
class illegal_move_exception(Exception):
    pass

class Board:
    b = None

    def clear(self):
        self.b = [
            [0 for j in range(board_size)]
            for i in range(board_size)
        ]

    def __init__(self, game_board = None):
        if(game_board is None):
            # Create a new empty board
            self.clear()

            # Initialize it with 2, 2 or 2, 4
            initializers = list(random.choice([
                (2, 4),
                (2, 2)
            ]))

            for y, x in random.sample(all_tiles, len(initializers)):
                self[y, x] = initializers.pop()
        elif(isinstance(game_board, Board)):
            # Copy constructor
            self.b = [
                [
                    game_board[y, x]
                    for x in range(board_size)
                ]
                for y in range(board_size)
            ]
        else:
            # Copy from lists
            self.b = [
                [
                    game_board[y][x]
                    for x in range(board_size)
                ]
                for y in range(board_size)
            ]

    def __getitem__(self, indices):
        return self.b[indices[0]][indices[1]]

    def __setitem__(self, indices, value):
        self.b[indices[0]][indices[1]] = value

    def __repr__(self):
        cell_size = max(len(str(self[y, x])) for y, x in all_tiles)
        line_size = (cell_size + 1) * board_size
        sep_line = "+".join("-" * (cell_size + 2) for i in range(board_size))

        ret = ""
        for y in range(board_size):
            for x in range(board_size):
                if(self[y, x] != 0):
                    ret += " " + (" " * cell_size + str(self[y, x]))[-cell_size:] + " "
                else:
                    ret += " " * (cell_size + 2)

                if(x != board_size - 1):
                    ret += "|"

            if(y != board_size - 1):
                ret += "\n" + sep_line + "\n"

        return ret + "\n"

    def move_tile(self, move):
        move_axis = move.get_move_axis()
        fixed_axis = move.get_static_axis()
        direction = sum(move.get_dir())

        done_something = False

        adapt = \
            lambda i: \
            i if(direction != 1) else (board_size - i - 1)

        conv_i_j = \
            lambda i, j: \
            (
                i if(fixed_axis == "y") else adapt(j),
                adapt(j) if(move_axis == "x") else i
            )

        def get(i, j):
            return self[conv_i_j(i, j)]

        def put(i, j, value):
            self[conv_i_j(i, j)] = value

        for i in range(board_size):
            last_stumbled = None
            last_stumbled_idx = None
            first_free_idx = None

            for j in range(board_size):
                cur = get(i, j)

                if(cur != 0):
                    if(last_stumbled == cur):
                        put(i, j, 0)
                        put(i, last_stumbled_idx, cur * 2)
                        first_free_idx = last_stumbled_idx + 1
                        last_stumbled = None
                        last_stumbled_idx = None
                        done_something = True
                    elif(first_free_idx is not None):
                        put(i, j, 0)
                        put(i, first_free_idx, cur)
                        last_stumbled = cur
                        last_stumbled_idx = first_free_idx
                        first_free_idx += 1
                        done_something = True
                    else:
                        last_stumbled_idx = j
                        last_stumbled = cur
                elif(first_free_idx is None):
                    first_free_idx = j

        if(not done_something):
            raise illegal_move_exception

    def get_legal_moves(self):
        ret = []
        for move in all_moves:
            try:
                Board(self).move_tile(move)
                ret.append(move)
            except(illegal_move_exception):
                continue

        return ret

    def has_legal_moves(self):
        return bool(self.get_legal_moves())

    def add_random_tile(self):
        try:
            self[random.choice(tuple(self.get_free_tiles()))] = random.choice(possible_new_tiles)
        except(IndexError):
            raise illegal_move_exception()

    def move(self, move):
        self.move_tile(move)
        self.add_random_tile()

    def has_tile(self, value):
        for y, x in all_tiles:
            if(self[y, x] == value):
                return True

        return False

    def get_max_tile(self):
        return max(self[y, x] for y, x in all_tiles)

    def get_free_tiles(self):
        return ((y, x) for y, x in all_tiles if(self[y, x] == 0))

    def get_num_free_tiles(self):
        return sum(1 for tile in self.get_free_tiles())
