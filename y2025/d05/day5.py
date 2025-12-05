import operator
from functools import reduce

import portion as P
from parsy import seq, string

from parsing import number, split_on_blank


def parse_range(line):
    return seq(number, string("-") >> number).map(tuple).parse(line)


with open("input.txt") as f:
    ranges, available = split_on_blank(f)
    ranges = [parse_range(line.rstrip()) for line in ranges]
    available = [int(line) for line in available]

print(ranges)
print(available)

fresh = reduce(operator.or_, (P.closed(left, right) for left, right in ranges))

print(sum(1 for ing in available if ing in fresh))

print(sum(atom.upper - atom.lower + 1 for atom in fresh))
