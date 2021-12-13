import re

def parse(line):
    [x, y] = line.strip().split(",")
    return int(x), int(y)

with open("input.txt") as f:
    line = f.readline()
    points = []
    while len(line.strip()) > 0:
        points.append(parse(line))
        line = f.readline()

    folds = [re.match(r"fold along (.)=(\d+)", line).groups() for line in f.readlines()]

# setup grid
grid = set(points)

# part 1
for dir, val in folds:
    val = int(val)
    if dir == "x":
        grid = set((x if x < val else 2 * val - x, y) for x, y in grid)
    else:
        grid = set((x, y if y < val else 2 * val - y) for x, y in grid)
    print(len(grid))

def draw_grid(grid):
    xmax = max(x for x,_ in grid)
    ymax = max(y for _,y in grid)
    for y in range(ymax+1):
        for x in range(xmax+1):
            print("*" if (x,y) in grid else " ", end="")
        print()

draw_grid(grid)
