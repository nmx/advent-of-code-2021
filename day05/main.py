import numpy as np
from numpy import ndarray


def main(filename, include_diagonal):
    with open(filename) as f:
        segments = [parse_line(line) for line in f.readlines()]

    max_x = max_coord(segments, 0)
    max_y = max_coord(segments, 1)
    floor = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    num_dangerous_points = 0
    for segment in segments:
        new_dangerous_points = mark_segment(floor, segment, include_diagonal)
        num_dangerous_points += new_dangerous_points

    print(f"Dangerous points: {num_dangerous_points}")


def parse_line(line):
    return [[int(x), int(y)] for x, y in [point.split(',') for point in line.strip().split(' -> ')]]


def max_coord(endpoints, idx):
    return max(ndarray.flatten(np.array([(p[0][idx], p[1][idx]) for p in endpoints])))


def mark_segment(floor, segment, include_diagonal):
    new_dangerous_points = 0
    start, end = segment
    if start[0] == end[0]:  # horizontal
        x = start[0]
        if start[1] > end[1]:
            start, end = end, start
        for y in range(start[1], end[1] + 1):
            if mark_point(floor, (x, y)):
                new_dangerous_points += 1
    elif start[1] == end[1]:  # vertical
        y = start[1]
        if start[0] > end[0]:
            start, end = end, start
        for x in range(start[0], end[0] + 1):
            if mark_point(floor, (x, y)):
                new_dangerous_points += 1
    elif include_diagonal:
        if start[1] > end[1]:
            start, end = end, start
        dec_x = start[0] > end[0]
        x = start[0]
        for y in range(start[1], end[1] + 1):
            if mark_point(floor, (x, y)):
                new_dangerous_points += 1
            x += (-1 if dec_x else 1)

    return new_dangerous_points


# Mark the point if it hasn't already been flagged as dangerous, and return if the point is newly considered dangerous.
def mark_point(floor, point):
    x, y = point
    if floor[y][x] == 2:
        return False
    elif floor[y][x] == 1:
        floor[y][x] += 1
        return True
    else:
        floor[y][x] += 1
        return False


def print_floor(floor):
    for line in floor:
        print(' '.join([str(point) for point in line]))


if __name__ == '__main__':
    main('input.txt', False)
    main('input.txt', True)
