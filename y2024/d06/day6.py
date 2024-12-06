from utils import in_bounds, coord_add


def parse(line):
    return [c for c in line]


with open("input.txt") as f:
    grid = [parse(line.rstrip()) for line in f]

def find_guard():
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '^':
                return r, c

guard_start = find_guard()

def walk_around() -> tuple[bool, set[tuple[int, int]]]:
    guard = guard_start

    # heading north
    move = (-1, 0)
    # where we've stepped
    visited = set()
    visited.add(guard)
    # transitions (guard, next) we bonked into obstacles
    bonked = set()
    next = coord_add(guard, move)
    while in_bounds(grid, *next):
        if grid[next[0]][next[1]] == '#':
            if (guard, next) in bonked:
                # this is a loop!
                return True, visited
            bonked.add((guard, next))
            # turn right
            move = (move[1], -move[0])
        else:
            # take the step
            guard = next
            visited.add(guard)
        next = coord_add(guard, move)
    return False, visited

_, visited = walk_around()
print(len(visited))

loop_count = 0
for (r, c) in visited:
    if grid[r][c] == '^':
        continue
    # add an obstacle
    grid[r][c] = '#'
    loop, _ = walk_around()
    grid[r][c] = '.'
    if loop:
        loop_count += 1
print(loop_count)
