from coord_utils import Coord2D, ORTHO_DIRS, DIAG_DIRS

with open("input.txt") as f:
    lines = [line.rstrip() for line in f]

PAPER = "@"
paper = {Coord2D(x, y) for y, row in enumerate(lines) for x, cell in enumerate(row) if cell == PAPER}

def reachable(coord):
    return sum(1 for dir in [*ORTHO_DIRS, *DIAG_DIRS] if (coord + dir) in paper) < 4

print(sum(1 for coord in paper if reachable(coord)))

removed = 0
while True:
    to_remove = {coord for coord in paper if reachable(coord)}
    if not to_remove: break
    removed += len(to_remove)
    paper -= to_remove

print(removed)
