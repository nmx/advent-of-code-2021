def main(filename, days):
    # array of buckets 0-8, each representing the number of fish with that counter value
    fish_by_counter = [0 for i in range(9)]
    for counter in read_counters(filename):
        fish_by_counter[counter] += 1

    for i in range(days):
        fish_by_counter = spawn(fish_by_counter)

    print(f"After {days} days: {sum(fish_by_counter)} fish")


def spawn(fish_by_counter):
    # rotate left
    res = fish_by_counter[1:] + fish_by_counter[:1]

    # fish that were in bucket 0 are now new fish in bucket 8. restore the original fish into bucket 6.
    res[6] += res[8]
    return res


def read_counters(filename):
    with open(filename) as f:
        return [int(counter) for counter in f.readline().strip().split(',')]


if __name__ == '__main__':
    main('input.txt', 80)
    main('input.txt', 256)
