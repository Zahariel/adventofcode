import operator
from functools import partial, reduce

from parsy import whitespace

from parsing import number

def parse(line):
    parser = number.sep_by(whitespace)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]


def extrapolate(history):
    diffs = [history[i+1]-history[i] for i in range(len(history) - 1)]
    if all(diff == 0 for diff in diffs):
        return history[0], history[-1]
    prev_diff, next_diff = extrapolate(diffs)
    return history[0] - prev_diff, history[-1] + next_diff

# note to readers: partial(map, operator.add) means lambda l, r: (l[0] + r[0], l[1] + r[1], ....)
# although in this case they're only two elements long
# PyTypeChecker doesn't understand partial correctly
# noinspection PyTypeChecker
print(tuple(reduce(partial(map, operator.add), (extrapolate(history) for history in lines))))
