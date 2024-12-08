import math
from collections import defaultdict
from itertools import combinations

from utils import in_bounds, Coord2D


def parse(line):
    return [c for c in line]


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

antennas = defaultdict(set)

HEIGHT = len(lines)
WIDTH = len(lines[0])

for r, row in enumerate(lines):
    for c, cell in enumerate(row):
        if cell == ".": continue
        antennas[cell].add(Coord2D(r, c))

antinodes = set()

for freq, locs in antennas.items():
    for left, right in combinations(locs, 2):
        vector = right - left
        antinodes.add(right + vector)
        antinodes.add(left - vector)

print(sum(1 for (r, c) in antinodes if in_bounds(lines, r, c)))

antinodes = set()

for freq, locs in antennas.items():
    for left, right in combinations(locs, 2):
        vector = right - left
        vgcd = math.gcd(*vector)
        vector = vector // vgcd
        for anti in left.ray(vector):
            if not in_bounds(lines, *anti):
                break
            antinodes.add(anti)
        for anti in left.ray(-vector):
            if not in_bounds(lines, *anti):
                break
            antinodes.add(anti)

print(len(antinodes))
