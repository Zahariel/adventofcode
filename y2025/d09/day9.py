from collections import defaultdict
from itertools import combinations, pairwise

from parsy import seq, string

from collection_utils import n_wise
from coord_utils import Coord2D
from parsing import number


def parse(line):
    return seq(number, string(",") >> number).combine(Coord2D).parse(line)


with open("input.txt") as f:
    red_tiles = [parse(line.rstrip()) for line in f]


def area(corner1, corner2):
    diag = corner1 - corner2
    return (abs(diag.x) + 1) * (abs(diag.y) + 1)

print(max(area(*pair) for pair in combinations(red_tiles, 2)))


NORTH = Coord2D(0, -1)
SOUTH = Coord2D(0, 1)
WEST = Coord2D(-1, 0)
EAST = Coord2D(1, 0)

def unit(dir):
    return Coord2D(0 if dir.x == 0 else dir.x // abs(dir.x), 0 if dir.y == 0 else dir.y // abs(dir.y))

edge_map = defaultdict(set)
for here, there in n_wise(red_tiles, 2, cyclic=True):
    dir = unit(there - here)
    for start, end in pairwise(here.ray(dir)):
        edge_map[start].add(dir)
        edge_map[end].add(-dir)
        if end == there:
            break


working = 0
def area2(corner1, corner2):
    global working
    working += 1
    if working % 1000 == 0:
        print(f"working {working}")
    left, top = corner1
    right, bottom = corner2
    if left > right:
        left, right = right, left
    if top > bottom:
        top, bottom = bottom, top
    # every cell of top and bottom edges of rectangle must be either an edge or inside
    for y in [top, bottom]:
        inside = set()
        for x in range(right+1):
            if (x, y) in edge_map:
                inside ^= edge_map[(x, y)]
            if x < left:
                continue
            if (x, y) not in edge_map and not (inside >= {NORTH, SOUTH}):
                return 0
    # every cell of left and right edges must be either an edge or inside
    for x in [left, right]:
        inside = set()
        for y in range(bottom+1):
            if (x, y) in edge_map:
                inside ^= edge_map[(x, y)]
            if y < top:
                continue
            if (x, y) not in edge_map and not (inside >= {WEST, EAST}):
                return 0
    # if it's fine, return the area
    return area(corner1, corner2)

print(max(area2(*pair) for pair in combinations(red_tiles, 2)))
