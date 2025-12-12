import functools
from typing import NamedTuple

import itertools
from parsy import seq, string, whitespace

from coord_utils import Coord2D
from parsing import number, split_on_blank

# this is correct but it's WAY WAY TOO SLOW OMG

class Region(NamedTuple):
    size: Coord2D
    requirements: list[int]


def parse(line):
    size = seq(number << string("x"), number << string(":")).combine(Coord2D)
    reqs = number.sep_by(whitespace)
    return seq(size << whitespace, reqs).combine(Region).parse(line)


with open("test.txt") as f:
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


def all_rotations(present):
    rotated = set(present)
    for i in range(4):
        yield rotated
        yield {Coord2D(2-x, y) for x, y in rotated}
        rotated = {Coord2D(y, 2-x) for x, y in rotated}


presents_rotated = [list(all_rotations(present)) for present in presents]


@functools.cache
def solve_helper(width, height, presents_needed, grid_taken, status=False):
    if not presents_needed: return True, []

    present_to_place = presents_rotated[presents_needed[0]]
    rest = tuple(presents_needed[1:])
    for x in range(width-2):
        for y in range(height-2):
            if status: print(f"{x}, {y}")
            for rot in present_to_place:
                placed = {Coord2D(x+dx, y+dy) for dx, dy in rot}
                if placed & grid_taken:
                    continue
                result, pieces = solve_helper(
                    width,
                    height,
                    rest,
                    grid_taken | placed,
                )
                if result:
                    return True, pieces + [placed]
    return False, []

def solve(region:Region):
    # this blob just turns [1, 0, 3, 2, 1] into (0, 2, 2, 2, 3, 3, 4)
    presents_needed = tuple(itertools.chain(*([i] * count for i, count in enumerate(region.requirements))))
    print(presents_needed)
    result, pieces = solve_helper(region.size.x, region.size.y, presents_needed, frozenset(), True)
    if result:
        print_solution(region, reversed(pieces))
    return result


def print_solution(region, pieces):
    grid = {coord: chr(ord('A') + idx) for idx, piece in enumerate(pieces) for coord in piece}
    for y in range(region.size.y):
        print("".join(grid.get((x, y), ".") for x in range(region.size.x)))

print(solve(regions[2]))
