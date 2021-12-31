from unittest import TestCase

from main import *


class Test(TestCase):
    def test_shift(self):
        scanner = [Point(1, 2, 3), Point(-1, -2, -3)]
        result = shift(scanner, Point(-3, -2, -1))
        self.assertEqual(result, [Point(-2, 0, 2), Point(-4, -4, -4)])

    def test_q1(self):
        # Sample beacons are from scanner 0's reference (which find_matches also enforces)
        sample_beacons = []
        with open('sample_beacons.txt') as f:
            for line in f.readlines():
                sample_beacons.append(Point(*[int(i) for i in line.strip().split(',')]))

        scanners = parse('sample.txt')

        for point in scanners[0].points:
            self.assertIn(point, sample_beacons)

        shifted, _ = check_for_overlap(scanners[0].points, scanners[1].points)
        for point in shifted:
            self.assertIn(point, sample_beacons)
        scanners = find_matches(scanners)
        for i in range(len(scanners)):
            for beacon in scanners[i].points:
                self.assertIn(beacon, sample_beacons, f"Check scanner {i}")

        self.assertEqual(count_beacons(scanners), 79)

    def test_q2(self):
        scanners = parse('sample.txt')
        scanners = find_matches(scanners)
        for i in range(len(scanners)):
            print(f"Offset: {scanners[i].offset}")
        self.assertEqual(greatest_manhattan_distance(scanners), 3621)
