import heapq


class Node(object):
    def __init__(self, grid, row, col, val):
        self.grid = grid
        self.row = row
        self.col = col
        self.val = val

        # treat None as infinity
        self.f = None
        self.g = None

        # reference for soft deletion from heap
        self.heap_ref = None

    def neighbors(self):
        if self.row > 0:
            # up
            yield self.grid[self.row - 1][self.col]
        if self.col < len(self.grid[self.row]) - 1:
            # right
            yield self.grid[self.row][self.col + 1]
        if self.row < len(self.grid) - 1:
            # down
            yield self.grid[self.row + 1][self.col]
        if self.col > 0:
            # left
            yield self.grid[self.row][self.col - 1]

    def copy_and_increment(self, dest_row, dest_col, i):
        new_val = self.val + i
        # assume we can only wrap once (since i <= 4)
        if new_val > 9:
            new_val = new_val % 10 + 1
        return Node(self.grid, dest_row, dest_col, new_val)

    def __gt__(self, other):
        return self.f > other.f


def q1(filename):
    grid = make_grid(filename)
    search_grid(grid)


def q2(filename):
    grid = make_grid(filename)
    expand_grid(grid, 5)
    search_grid(grid)


def search_grid(grid):
    start = grid[0][0]
    goal = grid[-1][-1]

    # treat None as infinity
    start.g = 0
    start.f = calc_h(start, goal)

    frontier = []
    update_heap_node(frontier, start)

    while frontier:
        current_node, delete_flag = heapq.heappop(frontier)
        if delete_flag:
            continue

        if current_node == goal:
            print(f"Found goal, minimum score {goal.f}")
            break

        for neighbor in current_node.neighbors():
            candidate_g = current_node.g + neighbor.val
            if neighbor.g is None or candidate_g < neighbor.g:
                neighbor.g = candidate_g
                neighbor.f = candidate_g + calc_h(neighbor, goal)
                update_heap_node(frontier, neighbor)
    else:
        raise RuntimeError("ran out of nodes")


# Make grid with position row=0, col=0 at the upper left. indices increase down and to the right
def make_grid(filename):
    with open(filename) as f:
        grid = []
        grid.extend([
            [Node(grid, row, col, int(val)) for col, val in enumerate(list(line.strip()))]
            for row, line in enumerate(f.readlines())
        ])
        return grid


# Expand grid by factor in all directions, increasing risk by 1 for each tile
def expand_grid(grid, factor):
    orig_num_rows = len(grid)
    orig_num_cols = len(grid[0])

    # expand right
    for row in range(orig_num_rows):
        for i in range(1, factor):
            for col in range(orig_num_cols):
                dest_col = i * orig_num_cols + col
                grid[row].append(grid[row][col].copy_and_increment(row, dest_col, i))

    # expand down
    for i in range(1, factor):
        for row in range(orig_num_rows):
            grid.append([])
            dest_row = i * orig_num_rows + row
            for col in range(len(grid[row])):
                grid[dest_row].append(grid[row][col].copy_and_increment(dest_row, col, i))


def push_heap(heap, node):
    assert not node.heap_ref
    entry = [node, False]
    node.heap_ref = entry
    heapq.heappush(heap, entry)


def update_heap_node(heap, node):
    if node.heap_ref:
        node.heap_ref[-1] = True
        node.heap_ref = None
    push_heap(heap, node)


def calc_h(node, goal):
    # Manhattan distance to goal
    return abs(node.col - goal.col) + abs(node.row - goal.row)


def print_grid(grid):
    for row in grid:
        print("".join([str(node.val) for node in row]))


if __name__ == '__main__':
    q1('input.txt')
    q2('input.txt')