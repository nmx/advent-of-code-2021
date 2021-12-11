from functools import reduce


def main(filename):
    grid = make_grid(filename)

    risk_level = 0
    basin_sizes = []
    risk_grid = ''
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            v = grid[i][j].val
            # look left
            if j > 0 and v >= grid[i][j - 1].val:
                risk_grid += '.'
                continue
            # look up
            if i > 0 and v >= grid[i -1][j].val:
                risk_grid += '.'
                continue
            # look right
            if j < len(grid[i]) - 1 and v >= grid[i][j + 1].val:
                risk_grid += '.'
                continue
            # look down
            if i < len(grid) - 1 and v >= grid[i + 1][j].val:
                risk_grid += '.'
                continue
            risk_grid += str(v)
            risk_level += v + 1
            basin_sizes.append(count_basin_around(grid, i, j, v))
        risk_grid += '\n'

    print(f"Risk grid:\n{risk_grid}")
    print(f"Q1 result: {risk_level}")
    print(f"Basins: {basin_sizes}")
    print(f"Q2 result: {reduce((lambda x, y: x * y), sorted(basin_sizes)[-3:])}")


def make_grid(filename):
    with open(filename) as f:
        return [[Point(i) for i in list(line.strip())] for line in f.readlines()]


def count_basin_around(grid, i, j, min_val):
    if i < 0 or j < 0 or i == len(grid) or j == len(grid[i]):
        return 0
    p = grid[i][j]

    if p.counted or p.val == 9:
        return 0

    if p.val < min_val:
        return 0

    p.mark_counted()
    sum = 1

    # search left
    sum += count_basin_around(grid, i, j - 1, p.val + 1)
    # search up
    sum += count_basin_around(grid, i - 1, j, p.val + 1)
    # search right
    sum += count_basin_around(grid, i, j + 1, p.val + 1)
    # search down
    sum += count_basin_around(grid, i + 1, j, p.val + 1)

    return sum


class Point(object):
    def __init__(self, char_val):
        self._val = int(char_val)
        self._counted = False

    @property
    def val(self):
        return self._val

    @property
    def counted(self):
        return self._counted

    def mark_counted(self):
        self._counted = True


if __name__ == '__main__':
    main('input.txt')