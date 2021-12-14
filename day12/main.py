class Graph(object):
    def __init__(self, filename):
        # use node label as dict key
        self._caves = {}
        with open(filename) as f:
            for line in f.readlines():
                src, dst = [self._add_cave(label) for label in line.strip().split('-')]
                src.add_edge(dst)
                dst.add_edge(src)

    def cave(self, label):
        return self._caves[label]

    def _add_cave(self, label):
        if label not in self._caves:
            self._caves[label] = Cave(label)
        return self._caves[label]


class Cave(object):
    def __init__(self, label):
        self._label = label
        self._visits = 0
        self._edges = []

    def add_edge(self, dst):
        self._edges.append(dst)

    @property
    def label(self):
        return self._label

    @property
    def edges(self):
        return self._edges

    def is_big(self):
        return self._label.isupper()

    @property
    def visits(self):
        return self._visits

    def visit(self):
        self._visits += 1

    def unvisit(self):
        self._visits -= 1


def main(filename):
    graph = Graph(filename)
    start = graph.cave('start')

    print(f"Q1 Paths: {find_paths(start, False)}")
    print(f"Q2 Paths: {find_paths(start, True)}")


path = ""


# returns the count of paths to 'end' found from the given cave
def find_paths(cave, allow_two_small_cave_visits):
    global path
    path += f"->{cave.label}"
    if cave.label == 'end':
        print(path)
        path = path[:-(len(cave.label) + 2)]
        return 1

    # don't count visits to big caves
    if not cave.is_big():
        cave.visit()
    if cave.visits == 2:
        allow_two_small_cave_visits = False

    paths = 0
    for edge in cave.edges:
        if can_visit(edge, allow_two_small_cave_visits):
            # If this cave has now been visited twice (for part 2),
            # don't allow any other small cave in the path to be
            # visited twice
            paths += find_paths(edge, allow_two_small_cave_visits)

    cave.unvisit()
    path = path[:-(len(cave.label) + 2)]
    return paths


def can_visit(cave, allow_two_small_cave_visits):
    return cave.label != 'start' \
        and (cave.visits < 1 or (cave.visits < 2 and allow_two_small_cave_visits))


if __name__ == '__main__':
    main('input.txt')
