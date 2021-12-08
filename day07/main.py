def main(filename, fuel_for_position_func):
    positions = read_positions(filename)
    max_position = max(positions)
    min_fuel_spent = None
    optimal_pos = None
    for pos in range(max_position + 1):
        fuel_spent = fuel_for_position_func(positions, pos)
        if min_fuel_spent is None or fuel_spent < min_fuel_spent:
            min_fuel_spent = fuel_spent
            optimal_pos = pos

    print(f"Optimal position: {optimal_pos} Fuel spent: {min_fuel_spent}")


def q1_fuel_for_position(positions, pos):
    fuel_spent = 0
    for original_position in positions:
        fuel_spent += abs(original_position - pos)
    return fuel_spent


def q2_fuel_for_position(positions, pos):
    fuel_spent = 0
    for original_position in positions:
        fuel_spent += sum_sequence(abs(original_position - pos))
    return fuel_spent


# sum from 1 to count, inclusive
def sum_sequence(count):
    return int((count / 2) * (2 + (count - 1)))


def read_positions(filename):
    with open(filename) as f:
        return [int(pos) for pos in f.readline().strip().split(',')]


if __name__ == '__main__':
    main('input.txt', q1_fuel_for_position)
    main('input.txt', q2_fuel_for_position)
