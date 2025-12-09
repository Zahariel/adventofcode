import bisect
from itertools import combinations

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


vert_edges: list[tuple[int, int, int]] = []
horiz_edges: list[tuple[int, int, int]] = []

# for start, end in [*pairwise(red_tiles), (red_tiles[-1], red_tiles[0])]:
for start, end in n_wise(red_tiles, 2, cyclic=True):
    if start.x == end.x:
        if start.y > end.y:
            start, end = end, start
        vert_edges.append((start.x, start.y, end.y))
    elif start.y == end.y:
        if start.x > end.x:
            start, end = end, start
        horiz_edges.append((start.y, start.x, end.x))
    else:
        raise ValueError

vert_edges.sort()
horiz_edges.sort()

# this tests strict intersection: treats all segments as open
def edges_intersect(horiz, vert):
    horiz_y, horiz_start, horiz_end = horiz
    vert_x, vert_start, vert_end = vert
    return vert_start < horiz_y < vert_end and horiz_start < vert_x < horiz_end

def is_safe(corner1, corner2):
    left, top = corner1
    right, bottom = corner2
    if left > right:
        left, right = right, left
    if top > bottom:
        top, bottom = bottom, top

    # shrink in from the edges to make the appropriate end closed
    # 0.5 here is standing in for "epsilon"
    # this is too conservative if there are two edges with no blank in between
    first_vert_edge = bisect.bisect_right(vert_edges, (left, 100000, 100000))
    last_vert_edge = bisect.bisect_left(vert_edges, (right, 0, 0))
    for vert_edge in vert_edges[first_vert_edge:last_vert_edge]:
        if edges_intersect((top+0.5, left, right), vert_edge): return False
        if edges_intersect((bottom-0.5, left, right), vert_edge): return False

    first_horiz_edge = bisect.bisect_right(horiz_edges, (top, 100000, 100000))
    last_horiz_edge = bisect.bisect_left(horiz_edges, (bottom, 0, 0))
    for horiz_edge in horiz_edges[first_horiz_edge:last_horiz_edge]:
        if edges_intersect(horiz_edge, (left+0.5, top, bottom)): return False
        if edges_intersect(horiz_edge, (right-0.5, top, bottom)): return False

    return True

print(max(area(*pair) for pair in combinations(red_tiles, 2) if is_safe(*pair)))
