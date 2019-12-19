from y2019.intcode import CoIntComp

with open("input.txt") as f:
    initial_cells = [int(c) for c in f.readline().strip().split(",")]


grid = [[False for x in range(50)] for y in range(50)]

def get_target(x, y):
    comp = CoIntComp(initial_cells)
    return comp.run(x, y) == 1

for y in range(50):
    for x in range(50):
        grid[y][x] = get_target(x, y)

print(sum(1 for row in grid for cell in row if cell))

def find_targets(y):
    x = 0
    while True:
        result = get_target(x, y)
        if result:
            break
        x = x + 1
    start_x = x
    while True:
        result = get_target(x, y)
        if not result:
            break
        x = x + 1
    end_x = x
    return start_x, end_x

# find first 101 cell row
SANTA_SIZE = 100
start_y = 20
max_y = None
min_y = None
while True:
    print(start_y)
    start_x, end_x = find_targets(start_y)
    if end_x - start_x > SANTA_SIZE:
        # this row is long enough
        max_y = start_y
    else:
        # this row isn't long enough
        min_y = start_y

    if min_y + 1 == max_y:
        start_y = max_y
        break

    if max_y is None:
        start_y = 2 * start_y
    else:
        start_y = (min_y + max_y) // 2

print()
print("row", start_y, "has", SANTA_SIZE + 1, "targeted squares")

curr_y = start_y
max_y = None
min_y = start_y
while True:
    start_x, end_x = find_targets(curr_y)
    other_corner = get_target(end_x - SANTA_SIZE, curr_y + SANTA_SIZE - 1)
    print(curr_y, start_x, end_x)
    if other_corner:
        max_y = curr_y
    else:
        min_y = curr_y

    if min_y + 1 == max_y:
        start_x, end_x = find_targets(max_y)
        break

    if max_y is None:
        curr_y = curr_y * 2
    else:
        curr_y = (min_y + max_y) // 2

print("square at", end_x - SANTA_SIZE, max_y)

print(end_x - 1, max_y - 1, get_target(end_x - 1, max_y - 1))
print(end_x, max_y, get_target(end_x, max_y))
print(end_x - SANTA_SIZE - 1, max_y + SANTA_SIZE - 1, get_target(end_x - SANTA_SIZE - 1, max_y + SANTA_SIZE - 1))
print(end_x - SANTA_SIZE, max_y + SANTA_SIZE, get_target(end_x - SANTA_SIZE, max_y + SANTA_SIZE))

print(end_x - SANTA_SIZE, max_y, get_target(end_x - SANTA_SIZE, max_y))
print(end_x - 1, max_y, get_target(end_x - 1, max_y))
print(end_x - SANTA_SIZE, max_y + SANTA_SIZE - 1, get_target(end_x - SANTA_SIZE, max_y + SANTA_SIZE - 1))
print(end_x - 1, max_y + SANTA_SIZE - 1, get_target(end_x - 1, max_y + SANTA_SIZE - 1))

for y in range(max_y - 5, max_y + SANTA_SIZE + 5):
    print(y, end=" ")
    for x in range(end_x - SANTA_SIZE - 5, end_x + 5):
        if get_target(x, y):
            if end_x - SANTA_SIZE <= x < end_x and max_y <= y <= max_y + SANTA_SIZE - 1:
                print("O", end="")
            else:
                print("#", end="")
        else:
            print(".", end="")
    print()