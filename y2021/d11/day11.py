def parse(line):
    return [int(c) for c in line.strip()]

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

def neighbors(y, x):
    top = y if y == 0 else y - 1
    bottom = y if y == 9 else y + 1
    left = x if x == 0 else x - 1
    right = x if x == 9 else x + 1
    return [(y2, x2) for y2 in range(top, bottom+1) for x2 in range(left, right+1) if (y2, x2) != (y, x)]

def step(grid):
    new_grid = [[c + 1 for c in row] for row in grid]
    flashes = set()
    processing = True
    while processing:
        processing = False
        for y, row in enumerate(new_grid):
            for x, c in enumerate(row):
                if (y,x) in flashes: continue
                if c > 9:
                    processing = True
                    flashes.add((y,x))
                    for i2, j2 in neighbors(y, x):
                        new_grid[i2][j2] += 1

    for y,x in flashes:
        new_grid[y][x] = 0

    return len(flashes), new_grid

# part 1
STEPS = 100
total = 0
grid = data
for i in range(STEPS):
    flashes, grid = step(grid)
    total += flashes

print(total)

# part 2
steps = STEPS
while True:
    flashes, grid = step(grid)
    steps += 1
    if flashes == 100:
        print(steps)
        break
