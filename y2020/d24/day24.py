import re
from collections import defaultdict

def parse(line):
    line = re.sub(r"([ns]?[we])", r"\1 ", line)
    return line.strip().split()


with open("input.txt") as f:
    paths = [parse(line.strip()) for line in f]


# all coords n, se, sw
DIRECTIONS = {
    'ne': (1, 0, -1),
    'e': (0, 1, -1),
    'se': (-1, 1, 0),
    'sw': (-1, 0, 1),
    'w': (0, -1, 1),
    'nw': (1, -1, 0),
}

def add_coords(left, right):
    return tuple(l + r for l, r in zip(left, right))

def follow_path(path):
    current = (0, 0, 0)
    for dir in path:
        move = DIRECTIONS[dir]
        current = add_coords(current, move)
    return current


blacks = set()
for path in paths:
    result = follow_path(path)
    if result in blacks:
        blacks.remove(result)
    else:
        blacks.add(result)

print(len(blacks))

# part 2: yup, it's hexagonal game of life

def generation(blacks):
    counts = defaultdict(int)
    for tile in blacks:
        counts[tile] += 1
        for dir in DIRECTIONS:
            counts[add_coords(tile, DIRECTIONS[dir])] += 1
    return set(new_tile for new_tile, count in counts.items() if count == 2 or (count == 3 and new_tile in blacks))

GENERATIONS = 100
for i in range(GENERATIONS):
    blacks = generation(blacks)
    print(i+1, len(blacks))
