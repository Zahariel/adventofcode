from coord_utils import in_bounds

MIRROR_NWSE = '\\'
MIRROR_NESW = '/'
SPLITTER_NS = '|'
SPLITTER_WE = '-'
EMPTY = '.'

def parse(line):
    return [c for c in line]

with open("input.txt") as file:
    grid = [parse(line.rstrip()) for line in file]


def one_laser_step(grid, r, c, dr, dc):
    cell = grid[r][c]
    if cell == MIRROR_NWSE:
        dr, dc = dc, dr
    elif cell == MIRROR_NESW:
        dr, dc = -dc, -dr
    elif cell == SPLITTER_NS:
        if dc != 0:
            return [(r - 1, c, -1, 0), (r + 1, c, 1, 0)]
    elif cell == SPLITTER_WE:
        if dr != 0:
            return [(r, c - 1, 0, -1), (r, c + 1, 0, 1)]
    return [(r + dr, c + dc, dr, dc)]

def evaluate(grid, start):
    lasers = [start]
    seen = set()
    heated = set()
    while len(lasers) > 0:
        r, c, dr, dc = lasers.pop()
        if not in_bounds(grid, r, c): continue
        if (r, c, dr, dc) in seen:
            continue
        seen.add((r, c, dr, dc))
        heated.add((r, c))
        lasers.extend(one_laser_step(grid, r, c, dr, dc))
    return heated

heated = evaluate(grid, (0, 0, 0, 1))
print(len(heated))


possible_starts = [
    *((r, 0, 0, 1) for r in range(len(grid))),
    *((r, len(grid[r]) - 1, 0, -1) for r in range(len(grid))),
    *((0, c, 1, 0) for c in range(len(grid[0]))),
    *((len(grid) - 1, c, -1, 0) for c in range(len(grid[-1]))),
]

print(max(len(evaluate(grid, start)) for start in possible_starts))

