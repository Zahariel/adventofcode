import portion as P
from parsy import seq, string

from parsing import number, split_on_blank


def parse_range(line):
    return seq(number, string("-") >> number).map(tuple).parse(line)


with open("input.txt") as f:
    ranges, available = split_on_blank(f)
    ranges = [parse_range(line.rstrip()) for line in ranges]
    available = [int(line) for line in available]

fresh = P.Interval(*(P.closedopen(left, right + 1) for left, right in ranges))

print(sum(1 for ing in available if ing in fresh))

print(sum(atom.upper - atom.lower for atom in fresh))
