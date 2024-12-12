from breadth_first import ortho_neighbors, breadth_first
from utils import ORTHO_DIRS, Coord2D


def parse(line):
    return [c for c in line]


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

HEIGHT = len(lines)
WIDTH = len(lines[0])
RAW_NEIGHBORS = ortho_neighbors((0, HEIGHT), (0, WIDTH))

grid = {(r, c):x for r, row in enumerate(lines) for c, x in enumerate(row)}

uncounted = {(r, c) for r in range(HEIGHT) for c in range(WIDTH)}

total = 0
regions = []

while uncounted:
    root = uncounted.pop()
    region = set()
    def process(_, loc):
        uncounted.discard(loc)
        region.add(Coord2D(*loc))
    def neighbors(loc):
        return [(1, nbr) for (_, nbr) in RAW_NEIGHBORS(loc) if grid[loc] == grid[nbr]]
    breadth_first(root, neighbors_fn=neighbors, process_fn=process)
    regions.append((grid[root], region))

def perimeter(region):
    return sum(1 for point in region for dir in ORTHO_DIRS if point + dir not in region)

print(sum(perimeter(region) * len(region) for _, region in regions))

def sides(region):
    # an edge segment (point, dir) counts if the tile in that direction is outside the region, AND the next
    # tile clockwise isn't a continuation of the same side
    return sum(1 for point in region for (dir, cw_dir) in zip(ORTHO_DIRS, ORTHO_DIRS[1:]+ORTHO_DIRS[:1])
               if point + dir not in region and (point + cw_dir not in region or point + cw_dir + dir in region))

print(sum(sides(region) * len(region) for _, region in regions))
