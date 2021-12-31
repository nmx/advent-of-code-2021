from collections import namedtuple
from typing import List, Optional, TextIO, Tuple
import re

Point = namedtuple('Point', 'x, y z')


class Scanner(object):
    def __init__(self, points: List[Point], offset: Point = Point(0, 0, 0), sorted_distances: List[int] = None):
        self.points = points
        self.offset = offset
        self.sorted_distances = sorted_distances if sorted_distances else calc_sorted_distances(points)

    def num_common_distances(self, other):
        matches = 0
        i = 0
        j = 0
        while i < len(self.sorted_distances) and j < len(other.sorted_distances):
            while i < len(self.sorted_distances) and self.sorted_distances[i] < other.sorted_distances[j]:
                i += 1
            if i == len(self.sorted_distances):
                break
            if self.sorted_distances[i] == other.sorted_distances[j]:
                matches += 1
                i += 1
                j += 1
            else:
                while j < len(other.sorted_distances) and self.sorted_distances[i] > other.sorted_distances[j]:
                    j += 1
        return matches



def main(filename: str):
    scanners = parse(filename)
    scanners = find_matches(scanners)
    print(f"Q1: {count_beacons(scanners)} beacons")
    print(f"Q1: {greatest_manhattan_distance(scanners)} is the greatest distance between scanners")


def calc_sorted_distances(points: List[Point]) -> List[int]:
    distances = []
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            distances.append(manhattan_distance(points[i], points[j]))
    return sorted(distances)


def find_matches(scanners: List[Scanner]) -> List[Scanner]:
    # There has to be at least one match with scanner 0. Use scanner 0 as the frame of reference for the remaining
    # scanners.
    fixed_scanners = [scanners[0]]
    unfixed_scanners = scanners[1:]

    while unfixed_scanners:
        find_match(fixed_scanners, unfixed_scanners)
    return fixed_scanners


def find_match(fixed_scanners: List[Scanner], unfixed_scanners: List[Scanner]) -> None:
    best_match = None
    best_match_score = -1
    for i in range(len(fixed_scanners)):
        for j in range(len(unfixed_scanners)):
            score = fixed_scanners[i].num_common_distances(unfixed_scanners[j])
            if score > best_match_score:
                best_match = (i, j)
                best_match_score = score

    i, j = best_match
    shifted_points, offset = check_for_overlap(fixed_scanners[i].points, unfixed_scanners[j].points)
    if not shifted_points:
        raise RuntimeError("Best apparent match was not actually a match")
    unfixed_scanner = unfixed_scanners.pop(j)
    fixed_scanners.append(Scanner(shifted_points, offset, unfixed_scanner.sorted_distances))


# return list of data from each scanner
def parse(filename: str) -> List[Scanner]:
    scanners = []
    with open(filename) as f:
        scanner = parse_one_scanner(f)
        while scanner:
            scanners.append(scanner)
            scanner = parse_one_scanner(f)
    return scanners


def parse_one_scanner(f: TextIO) -> Optional[Scanner]:
    line = f.readline()
    if not line:
        return None

    assert re.match(r'--- scanner ([0-9]+) ---', line) is not None
    line = f.readline()

    points = []
    while line.strip():
        points.append(Point(*[int(i) for i in line.strip().split(',')]))
        line = f.readline()
    return Scanner(points)


# Returns None if there weren't at least 12 matches, or, returns the rotated and shifted points of scanner B, in the
# same frame of reference as scanner A
def check_for_overlap(scanner_a: List[Point], scanner_b: List[Point]) -> Optional[Tuple[List[Point], Point]]:
    for rotated_b in generate_scanner_rotations(scanner_b):
        for candidate_a in scanner_a:
            for candidate_b in rotated_b:
                offset = vector_distance(candidate_b, candidate_a)
                shifted_b = shift(rotated_b, offset)
                set_b = set(shifted_b)
                matches = 0
                for point in scanner_a:
                    if point in set_b:
                        matches += 1
                if matches >= 12:
                    return shifted_b, offset
    return None


def generate_scanner_rotations(scanner: List[Point]) -> List[List[Point]]:
    rotations = [
        lambda p: Point( p.x,  p.y,  p.z),
        lambda p: Point( p.z,  p.y, -p.x),
        lambda p: Point(-p.x,  p.y, -p.z),
        lambda p: Point(-p.z,  p.y,  p.x),

        lambda p: Point(-p.x, -p.y,  p.z),
        lambda p: Point( p.z, -p.y,  p.x),
        lambda p: Point( p.x, -p.y, -p.z),
        lambda p: Point(-p.z, -p.y, -p.x),

        lambda p: Point( p.y, -p.x,  p.z),
        lambda p: Point( p.y, -p.z, -p.x),
        lambda p: Point( p.y,  p.x, -p.z),
        lambda p: Point( p.y,  p.z,  p.x),

        lambda p: Point(-p.y,  p.x,  p.z),
        lambda p: Point(-p.y, -p.z,  p.x),
        lambda p: Point(-p.y, -p.x, -p.z),
        lambda p: Point(-p.y,  p.z, -p.x),

        lambda p: Point( p.x, -p.z,  p.y),
        lambda p: Point(-p.z, -p.x,  p.y),
        lambda p: Point(-p.x,  p.z,  p.y),
        lambda p: Point( p.z,  p.x,  p.y),

        lambda p: Point( p.x,  p.z, -p.y),
        lambda p: Point( p.z, -p.x, -p.y),
        lambda p: Point(-p.x, -p.z, -p.y),
        lambda p: Point(-p.z,  p.x, -p.y)
    ]

    return [[rotation(p) for p in scanner] for rotation in rotations]


def vector_distance(a: Point, b: Point):
    return Point(b.x - a.x, b.y - a.y, b.z - a.z)


def manhattan_distance(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


def shift(scanner: List[Point], vector: Point) -> List[Point]:
    return [Point(point.x + vector.x, point.y + vector.y, point.z + vector.z) for point in scanner]


def count_beacons(scanners: List[Scanner]) -> int:
    beacons = set()
    for scanner in scanners:
        for p in scanner.points:
            beacons.add(p)
    return len(beacons)


def greatest_manhattan_distance(scanners: List[Scanner]) -> int:
    best = 0
    for i in range(len(scanners) - 1):
        for j in range(1, len(scanners)):
            best = max(best, manhattan_distance(scanners[i].offset, scanners[j].offset))
    return best


if __name__ == '__main__':
    main('input.txt')
