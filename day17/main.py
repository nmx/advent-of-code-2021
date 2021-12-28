from collections import namedtuple

Range = namedtuple('Range', ['lower', 'upper'])


# location or velocity
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Probe(object):
    def __init__(self, initial_velocity):
        self.velocity = initial_velocity
        self.position = Point(0, 0)

    def step(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        if self.velocity.x < 0:
            self.velocity.x += 1
        elif self.velocity.x > 0:
            self.velocity.x -= 1
        self.velocity.y -= 1


def main(filename):
    x_range, y_range = parse(filename)

    possible_x_velocities = find_possible_x_velocities(x_range)
    possible_y_velocities = find_possible_y_velocities(y_range)

    max_y = 0
    valid_solutions = 0
    for vx in possible_x_velocities:
        for vy in possible_y_velocities:
            max_y_observed = max_y_for_initial_velocity(Point(vx, vy), x_range, y_range)
            if max_y_observed is not None:
                valid_solutions += 1
                if max_y_observed > max_y:
                    max_y = max_y_observed

    print(f"Max y: {max_y}")
    print(f"Valid solutions: {valid_solutions}")


def find_possible_x_velocities(x_range):
    # It's cheap enough to iterate over all x up to the right edge of the target area
    return range(1, x_range.upper + 1)

def find_possible_y_velocities(y_range):
    # vy when it reaches the ground is -(starting vy) - make sure the next step will not overshoot the
    # bottom of the target area. and we can't start below the target area.
    return range(y_range.lower, abs(y_range.lower))


# return None if initial velocity won't reach the target
def max_y_for_initial_velocity(initial_velocity, x_range, y_range):
    probe = Probe(initial_velocity)
    max_y = probe.position.y
    while not missed_target(probe, x_range, y_range):
        probe.step()
        max_y = max(max_y, probe.position.y)
        if in_target_range(probe, x_range, y_range):
            return max_y
    else:
        return None


# return x_range, y_range
def parse(filename):
    with open(filename) as f:
        x_str, y_str = [xy for xy in f.readline().strip("\n").replace("target area: ", "").split(", ")]
    return [Range(*[int(i) for i in xy.split("=")[1].split("..")]) for xy in (x_str, y_str)]


def in_target_range(probe, x_range, y_range):
    return x_range.lower <= probe.position.x <= x_range.upper and y_range.lower <= probe.position.y <= y_range.upper


def missed_target(probe, x_range, y_range):
    return probe.position.y < y_range.lower or probe.position.x > x_range.upper


if __name__ == '__main__':
    main('input.txt')