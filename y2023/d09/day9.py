from parsy import whitespace

from parsing import number

def parse(line):
    parser = number.sep_by(whitespace)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]


def extrapolate(history):
    diffs = [history[i+1]-history[i] for i in range(len(history) - 1)]
    if set(diffs) == {0}:
        return history[-1]
    next_diff = extrapolate(diffs)
    return history[-1] + next_diff

print(sum(extrapolate(history) for history in lines))


def reverse_extrapolate(history):
    diffs = [history[i+1]-history[i] for i in range(len(history) - 1)]
    if set(diffs) == {0}:
        return history[0]
    prev_diff = reverse_extrapolate(diffs)
    return history[0] - prev_diff

print(sum(reverse_extrapolate(history) for history in lines))
