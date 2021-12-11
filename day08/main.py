from collections import defaultdict

# ordered 0-9
STANDARD_DIGIT_PATTERNS = [
    'abcefg',
    'cf',
    'acdeg',
    'acdfg',
    'bcdf',
    'abdfg',
    'abdefg',
    'acf',
    'abcdefg',
    'abcdfg'
]

DIGITS_BY_LEN = defaultdict(list)
for digit in range(10):
    DIGITS_BY_LEN[len(STANDARD_DIGIT_PATTERNS[digit])].append(digit)


def q1(filename):
    with open(filename) as f:
        outputs = [line.strip().split(' | ')[1] for line in f.readlines()]

    num_matches = 0
    for output in outputs:
        output_digits = output.split(' ')
        for output_digit in output_digits:
            digits_with_len = DIGITS_BY_LEN[len(output_digit)]
            if len(digits_with_len) == 1:  # easy case!
                num_matches += 1

    print(f"Matches by length: {num_matches}")


def sort_string(string):
    return ''.join(sorted(string))


def split_patterns(patterns):
    return [sort_string(pattern) for pattern in patterns.split(' ')]


def q2(filename):
    total = 0
    with open(filename) as f:
        for line in f.readlines():
            decoded = decode(line.strip())
            total += decoded
    print(f"Total sum: {total}")


def decode(line):
    signal_patterns, output_digits = [split_patterns(part) for part in line.split(' | ')]

    signal_mapping_dict, digit_patterns = try_permutations(signal_patterns, list('abcdefg'), 0)
    digit_patterns_to_digits = {pattern: n for n, pattern in enumerate(digit_patterns)}
    decoded_output = int(''.join([str(digit_patterns_to_digits[digit]) for digit in output_digits]))
    return decoded_output


def try_permutations(signal_patterns, signal_mapping_arr, i):
    res = try_mapping(signal_patterns, signal_mapping_arr)
    if res:
        return res
    if i == len(signal_mapping_arr) - 1:
        return
    for j in range(i, len(signal_mapping_arr)):
        copy = signal_mapping_arr.copy()
        swap(copy, i, j)
        res = try_permutations(signal_patterns, copy[:(i + 1)] + copy[(i + 1):], i + 1)
        if res:
            return res


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def try_mapping(signal_patterns, signal_mapping_arr):
    # Map from standard signal to remapped segment
    signal_mapping_dict = signal_mapping_arr_to_dict(signal_mapping_arr)
    digit_patterns = generate_digit_patterns(signal_mapping_dict)
    if is_valid_mapping(signal_patterns, digit_patterns):
        return signal_mapping_dict, digit_patterns
    else:
        return None


def signal_mapping_arr_to_dict(signal_mapping_arr):
    return {chr(ord('a') + n): char for n, char in enumerate(signal_mapping_arr)}


def is_valid_mapping(signal_patterns, digit_patterns):
    signal_pattern_set = set(signal_patterns)
    digit_pattern_set = set(digit_patterns)

    for signal_pattern in signal_pattern_set:
        if signal_pattern not in digit_pattern_set:
            # print(f"Missing {signal_pattern} from {digit_patterns}")
            return False
    return True


def generate_digit_patterns(signal_mapping_dict):
    # ordered 0-9
    digit_patterns = [
        sort_string(signal_mapping_dict[segment] for segment in standard_pattern)
        for standard_pattern in STANDARD_DIGIT_PATTERNS
    ]
    return digit_patterns


if __name__ == '__main__':
    q1('input.txt')
    q2('input.txt')
