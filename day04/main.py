import re

BOARD_SIZE = 5  # 5 rows x 5 columns


class BingoSquare(object):
    def __init__(self, val):
        self._val = val
        self._marked = False

    @property
    def val(self):
        return self._val

    @property
    def marked(self):
        return self._marked

    """If the value matches, mark the square and return True."""
    def mark(self, val):
        if self._val == val:
            self._marked = True
            return True
        return False

    def __str__(self):
        return f"{self._val:2}({'x' if self._marked else ' '})"


class BingoBoard(object):
    def __init__(self, rows):
        self._rows = rows
        self._is_winner = False

    """ Return True if any square was marked."""
    def mark(self, val):
        for row in self._rows:
            for square in row:
                if square.mark(val):
                    self._is_winner = self._has_row_win() or self._has_column_win()
                    return True
        return False

    def is_winner(self):
        return self._is_winner

    def _has_row_win(self):
        for row in self._rows:
            for col in row:
                if not col.marked:
                    break
            else:
                # no columns in the row were unmarked
                return True
        return False

    def _has_column_win(self):
        for c in range(BOARD_SIZE):
            for r in range(BOARD_SIZE):
                if not self._rows[r][c].marked:
                    break
            else:
                # no rows in the column were unmarked
                return True
        return False

    def sum_unmarked(self):
        score = 0
        for row in self._rows:
            for col in row:
                if not col.marked:
                    score += col.val
        return score

    def __str__(self):
        return 'Board=[\n' \
               + '\n'.join([' '.join([str(square) for square in row]) for row in self._rows]) \
               + '\n]'


def parse_draw_order(f):
    return [int(val) for val in f.readline().split(',')]


def parse_board(f):
    line = f.readline()  # read blank line between boards
    if not line:
        return None

    rows = []
    for i in range(BOARD_SIZE):
        line = f.readline().strip()
        rows.append([BingoSquare(int(val)) for val in re.findall(r'[^ ]+', line)])
    return BingoBoard(rows)


class Game(object):
    def __init__(self, filename):
        with open(filename) as f:
            self._draw_order = parse_draw_order(f)
            self._boards = []

            while True:
                board = parse_board(f)
                if not board:
                    break
                self._boards.append(board)

        self._winning_number = None
        self._winning_board = None

    def play_to_win(self):
        while not self._winning_board:
            self.call_next(False)
        self.print_winner()

    def let_the_squid_win(self):
        while self._draw_order:
            self.call_next(True)
        self.print_winner()

    def print_winner(self):
        unmarked_sum = self._winning_board.sum_unmarked()
        print(f"Winning number: {self._winning_number}")
        print(f"Winning board: {self._winning_board}")
        print(f"Unmarked sum: {unmarked_sum}")
        print(f"Final score: {self._winning_board.sum_unmarked() * self._winning_number}")

    def call_next(self, check_all_boards):
        val = self._draw_order.pop(0)
        for board in self._boards:
            # Don't consider boards that have already won (this only
            # matters if we are looking for the last-place board)
            if (not board.is_winner()) and board.mark(val):
                if board.is_winner():
                    self._winning_number = val
                    self._winning_board = board
                    # It is possible for multiple boards to win on the same number.
                    # Continue checking boards unless we only care about the first winner.
                    if not check_all_boards:
                        return


if __name__ == '__main__':
    print("Part 1:")
    Game('input.txt').play_to_win()

    print("\nPart 2:")
    Game('input.txt').let_the_squid_win()
