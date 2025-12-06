from parsy import seq, string, regex, whitespace

from parsing import number


def parse(line):
    return line


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

