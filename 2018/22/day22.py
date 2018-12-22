import heapq

depth = 8103
target_x, target_y = 9, 758
# depth = 510
# target_x, target_y = 10, 10


chars = [".", "=", "|"]
def print_cave(cave):
    for row in cave:
        for (_, cell) in row:
            print(chars[cell], end="")
        print()
    print()

def safe_calc_cell(cave, x, y):
    if y < len(cave) and x < len(cave[y]): return cave[y][x]
    # print("calc", x, y)
    if y == 0: index = 16807 * x
    elif x == 0: index = 48271 * y
    else:
        above, _ = safe_calc_cell(cave, x, y-1)
        left, _ = safe_calc_cell(cave, x-1, y)
        index = above * left
    level = (index + depth) % 20183
    while y >= len(cave):
        cave.append([])
    if x > len(cave[y]):
        safe_calc_cell(cave, x-1, y)
    cave[y].append((level, level % 3))
    return cave[y][x]

cave = [[(0,0)]]

cave[0][0] = (depth, depth % 3)
safe_calc_cell(cave, target_x, target_y)
cave[target_y][target_x] = (depth, depth % 3)
# print_cave(cave)
print(sum(cell for row in cave for (_, cell) in row))

# these are the same as the gear you can't use in the given region
NOTHING = 0
TORCH = 1
CLIMBING = 2

def neighbors(x, y):
    # make sure to add these in order
    yield x, y-1
    yield x-1, y
    yield x+1, y
    yield x, y+1

def in_bounds(grid, x, y):
    return 0 <= y and 0 <= x

def travel(grid):
    # seen has x, y, tool
    seen = set()
    # queue has time taken, x, y, tool equipped
    queue = [(0, 0, 0, 1)]
    while len(queue) > 0:
        time, x, y, tool = heapq.heappop(queue)
        if (x, y, tool) in seen: continue
        seen.add((x, y, tool))
        # print(time, x, y, tool)
        if (x, y) == (target_x, target_y):
            if tool == 1:
                return time
            else:
                heapq.heappush(queue, (time+7, x, y, 1))
                continue
        for nx, ny in neighbors(x, y):
            if in_bounds(grid, nx, ny):
                _, new_type = safe_calc_cell(grid, nx, ny)
                if tool != new_type:
                    heapq.heappush(queue, (time + 1, nx, ny, tool))
                else:
                    # have to switch to the tool that can be used in both regions
                    new_tool = 3 - grid[y][x][1] - new_type
                    heapq.heappush(queue, (time + 8, nx, ny, new_tool))
    return 0

print(travel(cave))
