from collections import namedtuple

Point = namedtuple("Point", "x y")
Fold = namedtuple("Fold", "axis val")


def main(filename):
    points, folds = parse(filename)

    max_x, max_y = max([point.x for point in points]), max([point.y for point in points])
    grid = [[False for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for point in points:
        grid[point.y][point.x] = True

    grid = fold_grid(grid, folds.pop(0))
    part_1_dots = count_dots(grid)
    print(f"Part 1: {part_1_dots} dots")

    print(f"Part 2: After final fold:")
    for fold in folds:
        grid = fold_grid(grid, fold)
    print_grid(grid)


def parse(filename):
    points = []
    folds = []

    with open(filename) as f:
        line = f.readline()
        while line != '\n':
            points.append(Point(*[int(v) for v in line.strip().split(',')]))
            line = f.readline()

        line = f.readline()
        while line:
            components = line.strip().replace('fold along ', '').split('=')
            folds.append(Fold(*(components[0], int(components[1]))))
            line = f.readline()

    return points, folds


def print_grid(grid):
    for line in grid:
        print(''.join(['#' if v else '.' for v in line]))


def fold_grid(grid, fold):
    if fold.axis == 'y':
        # Fold up
        dst_y = fold.val - 1
        for src_y in range(fold.val + 1, len(grid)):
            for x in range(len(grid[dst_y])):
                grid[dst_y][x] = grid[dst_y][x] or grid[src_y][x]
            dst_y -= 1
        return grid[:fold.val]
    else:
        # Fold left
        for y in range(len(grid)):
            dst_x = fold.val - 1
            for src_x in range(fold.val + 1, len(grid[y])):
                grid[y][dst_x] = grid[y][dst_x] or grid[y][src_x]
                dst_x -= 1
            grid[y] = grid[y][:fold.val]
        return grid


def count_dots(grid):
    return sum([sum(line) for line in grid])


if __name__ == '__main__':
    main('input.txt')
