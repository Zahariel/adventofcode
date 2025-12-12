from collections import defaultdict
from typing import NamedTuple

import itertools
import z3
from parsy import seq, string, whitespace
from z3 import IntSort

from coord_utils import Coord2D
from parsing import number, split_on_blank


# this is correct but it's WAY WAY TOO SLOW even in Z3!

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
    rotated = list(present)
    for i in range(4):
        yield rotated
        yield [Coord2D(2-x, y) for x, y in rotated]
        rotated = [Coord2D(y, 2-x) for x, y in rotated]


presents_rotated = [list(all_rotations(present)) for present in presents]

def solve(region:Region):
    s = z3.Solver()

    present_id = z3.Array("present_id", z3.IntSort(), z3.ArraySort(z3.IntSort(), z3.IntSort()))
    presents_needed = list(itertools.chain(*([i] * count for i, count in enumerate(region.requirements))))
    present_xs = [z3.Int(f"present_{i}_x") for i in range(len(presents_needed))]
    present_ys = [z3.Int(f"present_{i}_y") for i in range(len(presents_needed))]
    present_trs = [z3.Int(f"present_{i}_tr") for i in range(len(presents_needed))]
    for xvar in present_xs:
        s.add(xvar >= 0)
        s.add(xvar < region.size.x - 2)
    for yvar in present_ys:
        s.add(yvar >= 0)
        s.add(yvar < region.size.y - 2)
    for trvar in present_trs:
        s.add(trvar >= 0)
        s.add(trvar < 8)

    # inject the transformations into z3
    # present type id -> transform number (0-7) -> block number (arbitrary) -> d_coord
    CoordSort, MkCoord, [COORD_X, COORD_Y] = z3.TupleSort("Coords", [IntSort(), IntSort()])
    z3_transforms = z3.Array("all_transforms", z3.IntSort(), z3.ArraySort(z3.IntSort(), z3.ArraySort(z3.IntSort(), CoordSort)))
    for idx, present in enumerate(presents_rotated):
        for trans_id, trans in enumerate(present):
            for block_id, block in enumerate(trans):
                s.add(z3_transforms[idx][trans_id][block_id] == MkCoord(block.x, block.y))

    for idx, present_type in enumerate(presents_needed):
        for block_id in range(len(presents[present_type])):
            block_x = present_xs[idx] + COORD_X(z3_transforms[present_type][present_trs[idx]][block_id])
            block_y = present_ys[idx] + COORD_Y(z3_transforms[present_type][present_trs[idx]][block_id])
            s.add(present_id[block_x][block_y] == idx)

    result = s.check()
    if result == z3.sat:
        model = s.model()
        to_print = defaultdict(lambda: ".")
        for present_id, present_type in enumerate(presents_needed):
            present_x = model.eval(present_xs[present_id]).as_long()
            present_y = model.eval(present_ys[present_id]).as_long()
            present_tr = model.eval(present_trs[present_id]).as_long()
            for block in presents_rotated[present_type][present_tr]:
                to_print[Coord2D(present_x, present_y) + block] = chr(ord("A") + present_id)

        for y in range(region.size.y):
            print("".join(to_print[x, y] for x in range(region.size.x)))

    return result == z3.sat

print(solve(regions[2]))
