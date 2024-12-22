import operator

from coord_utils import in_bounds

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

connections = {
    '.': {},
    '|': {NORTH, SOUTH},
    '-': {WEST, EAST},
    'L': {NORTH, EAST},
    'J': {NORTH, WEST},
    '7': {WEST, SOUTH},
    'F': {EAST, SOUTH},
    'S': None,
}

def parse(line):
    return [connections[c] for c in line]

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

def add_coords(r, c, dir):
    return tuple(map(operator.add, (r, c), dir))

sr, sc = next((r, c) for r, line in enumerate(lines) for c, cell in enumerate(line) if cell is None)

lines[sr][sc] = set()
if in_bounds(lines, sr - 1, sc) and SOUTH in lines[sr-1][sc]: lines[sr][sc].add(NORTH)
if in_bounds(lines, sr + 1, sc) and NORTH in lines[sr+1][sc]: lines[sr][sc].add(SOUTH)
if in_bounds(lines, sr, sc - 1) and EAST in lines[sr][sc-1]: lines[sr][sc].add(WEST)
if in_bounds(lines, sr, sc + 1) and WEST in lines[sr][sc+1]: lines[sr][sc].add(EAST)


def opposite(dir):
    return tuple(map(operator.neg, dir))

def one_step(r, c, entrydir):
    potentials = set(lines[r][c])
    potentials.remove(opposite(entrydir))
    move = next(iter(potentials))
    return add_coords(r, c, move), move

def follow_loop(sr, sc):
    ending_move = opposite(next(iter(lines[sr][sc])))
    steps = [(sr, sc)]
    pos, dir = one_step(sr, sc, ending_move)
    while pos != (sr, sc):
        steps.append(pos)
        pos, dir = one_step(*pos, dir)
    assert(dir == ending_move)
    return steps

path = follow_loop(sr, sc)
print(len(path) // 2)


# part 2
pathset = set(path)
area = 0
for r, line in enumerate(lines):
    inside = set()
    for c, cell in enumerate(line):
        if (r, c) in pathset:
            inside = inside ^ cell
        elif inside >= {NORTH, SOUTH}:
            area += 1
print(area)


# part 2, an alternate solution based on Pick's theorem
def edge_area(r1, c1, r2, c2):
    return (r1 * c2 - r2 * c1) / 2
true_area = int(sum(edge_area(*path[i-1], *path[i]) for i in range(len(path))))
print(true_area - len(path) // 2 + 1)

