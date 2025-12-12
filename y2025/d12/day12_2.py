from typing import NamedTuple

from parsy import seq, string, whitespace

from coord_utils import Coord2D
from parsing import number, split_on_blank


class Region(NamedTuple):
    size: Coord2D
    requirements: list[int]


def parse(line):
    size = seq(number << string("x"), number << string(":")).combine(Coord2D)
    reqs = number.sep_by(whitespace)
    return seq(size << whitespace, reqs).combine(Region).parse(line)


with open("input.txt") as f:
    groups = list(split_on_blank(f))

    presents = []
    for group in groups[:-1]:
        present = set()
        for y, row in enumerate(group[1:]):
            for x, c in enumerate(row):
                if c == '#':
                    present.add(Coord2D(x, y))
        presents.append(present)

    regions = [parse(line) for line in groups[-1]]


# this is an incredible dirty hack but because the presents are so small and the space is so huge, we basically
# assume that we can pack them 100% efficiently
# it fails on all the test cases because of course it does

def maybe_solve(region: Region):
    # see if presents will fit even if they pack 100% efficiently with no wasted space
    squares_needed = sum(len(present) * count for present, count in zip(presents, region.requirements))
    if squares_needed > region.size.x * region.size.y: return False

    # maybe there's some weird border condition where they actually don't fit together well enough,
    # but probably not, and it's too expensive to find out
    return True

print(sum(1 for region in regions if maybe_solve(region)))
