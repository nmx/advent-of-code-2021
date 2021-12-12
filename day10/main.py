import math


OPEN_TO_CLOSE = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

CLOSE_TO_OPEN = {v: k for k, v in OPEN_TO_CLOSE.items()}

CORRUPT_POINT_MAP = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

AUTOCOMPLETE_POINT_MAP = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def main(filename):
    total_corrupt_score = 0
    autocomplete_scores = []
    with open(filename) as f:
        for line in f.readlines():
            corrupt_score, autocomplete_score = score_line(line)
            total_corrupt_score += corrupt_score
            if autocomplete_score:
                autocomplete_scores.append((autocomplete_score))
    print(f"Q1 total corrupt score: {total_corrupt_score}")
    print(f"Q2 median autocomplete score: {sorted(autocomplete_scores)[math.floor(len(autocomplete_scores) / 2)]}")


# returns (corrupt_score, autocomplete_score) for the line, where exactly one of the scores will be non-zero
def score_line(line):
    # the expected closing characters for the open chunks
    open_stack = []

    for c in line.strip():
        if c in OPEN_TO_CLOSE:
            open_stack.append(OPEN_TO_CLOSE[c])
        elif c != open_stack.pop():
            return CORRUPT_POINT_MAP[c], 0

    autocomplete_score = 0
    while open_stack:
        autocomplete_score = (autocomplete_score * 5) + AUTOCOMPLETE_POINT_MAP[open_stack.pop()]
    return 0, autocomplete_score


if __name__ == '__main__':
    main('input.txt')
