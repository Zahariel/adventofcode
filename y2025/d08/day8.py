import heapq
from itertools import combinations

from parsy import string

from coord_utils import Coord3D
from parsing import number
from unionfind import UnionFind


def parse(line):
    return number.sep_by(string(","), min=3, max=3).combine(Coord3D).parse(line)


with open("input.txt") as f:
    boxes = [parse(line.rstrip()) for line in f]

union_find = UnionFind(boxes)

CONNECTIONS = 1000
joins = [((left - right).magnitude, left, right) for left, right in combinations(boxes, 2)]
heapq.heapify(joins)

for _ in range(CONNECTIONS):
    _, left, right = heapq.heappop(joins)
    union_find.union(left, right)

circuits = union_find.to_sets()

c1, c2, c3 = heapq.nlargest(3, circuits, key=len)

print(len(c1) * len(c2) * len(c3))

while union_find.size > 1:
    _, left, right = heapq.heappop(joins)
    union_find.union(left, right)

print(left.x * right.x)
