from collections import defaultdict


def main(filename, steps):
    template, pairs, rules = parse(filename)

    for i in range(steps):
        step(pairs, rules)

    freqs = sorted([v for _, v in frequency_map(pairs, template).items()])
    print(f"Result after {steps} steps: {freqs[-1] - freqs[0]}")


def parse(filename):
    with open(filename) as f:
        polymer = f.readline().strip()
        pairs = polymer_to_pairs(polymer)

        f.readline()
        rules = {k: v for k, v in [line.strip().split(' -> ') for line in f.readlines()]}

    return polymer, pairs, rules


def polymer_to_pairs(polymer):
    pairs = defaultdict(int)
    for i in range(1, len(polymer)):
        pairs[polymer[i-1:i+1]] += 1
    return pairs


def step(pairs, rules):
    pairs_copy = pairs.copy()
    for pair, count in pairs_copy.items():
        pairs[pair[0] + rules[pair]] += count
        pairs[rules[pair] + pair[1]] += count
        pairs[pair] -= count


def frequency_map(pairs, template):
    result = defaultdict(int)
    for pair, count in pairs.items():
        result[pair[0]] += count
    # The above fails to count the last element in the original template
    # (which is still the last element in the result)
    result[template[-1]] += 1

    return result


if __name__ == '__main__':
    main('input.txt', 10)
    main('input.txt', 40)
