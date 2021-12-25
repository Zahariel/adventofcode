def parse(line):
    return list(line.rstrip())

with open("input.txt") as f:
    data = [parse(line) for line in f.readlines()]


def step(grid):
    future = [list(row) for row in grid]
    moved = False
    # first move rightwards
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != ">": continue
            target = (x + 1) % len(row)
            if grid[y][target] != ".": continue
            future[y][x] = '.'
            future[y][target] = '>'
            moved = True

    grid = future
    future = [list(row) for row in grid]
    # then move down
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != "v": continue
            target = (y + 1) % len(grid)
            if grid[target][x] != ".": continue
            future[y][x] = '.'
            future[target][x] = 'v'
            moved = True

    return moved, future

def print_grid(grid):
    for row in grid:
        print("".join(row))

grid = data
print(grid)
moved = True
steps = 0
while moved:
    moved, grid = step(grid)
    steps += 1
    print(steps)
    # print_grid(grid)
print("done in", steps)
