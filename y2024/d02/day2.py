import itertools

from parsy import whitespace

from parsing import number


def parse(line):
    return number.sep_by(whitespace).parse(line)

with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

def test(line):
    dir = (line[0] < line[1])
    return all((l < r) == dir and 1 <= abs(l - r) <= 3 for (l, r) in itertools.pairwise(line))

print(sum(1 for line in lines if test(line)))

def test2(line):
    if test(line): return True
    return any(test(line[:i] + line[i+1:]) for i in range(len(line)))

print(sum(1 for line in lines if test2(line)))
