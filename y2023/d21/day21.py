import operator
from functools import reduce

from breadth_first import breadth_first, ortho_neighbors

GARDEN = '.'
ROCK = '#'
START = 'S'
PART1_STEPS = 64
PART2_STEPS = 26501365


def parse(line):
    return [c for c in line]

def find_start():
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == START:
                grid[r][c] = GARDEN
                return r, c

with open("input.txt") as file:
    grid = [parse(line.rstrip()) for line in file]

start = find_start()
startr, startc = start

def step_one(r, c):
    for _, (r2, c2) in ortho_neighbors((0, len(grid)), (0, len(grid[0])))((r, c)):
        if grid[r2][c2] == GARDEN:
            yield (r2, c2)


def step(current_spots):
    result = set()
    for spot in current_spots:
        result.update(step_one(*spot))
    return result

locs = {start}
for i in range(PART1_STEPS):
    locs = step(locs)

print(len(locs))



# this relies on the grid being an odd-sized square and start being in the exact center
# and that the edges of the grid, as well as the row/column with start, are free of rocks
# unfortunately, the example doesn't satisfy these requirements: it has rocks in the start column

# this is the number of grids i can go from the start and still reach the far corners
with open("input.txt") as file:
    grid = [parse(line.rstrip()) for line in file]

start = find_start()
startr, startc = start
print(start)


full_grids = (PART2_STEPS - startr - startc) // len(grid)
leftover_steps_straight = PART2_STEPS - startr - (full_grids * len(grid)) - 1
leftover_steps_corner = PART2_STEPS - startr - startc - (full_grids * len(grid)) - 2


rocks = {(r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == ROCK}
def neighbors(pos):
    for cost, pos2 in ortho_neighbors((0, len(grid)), (0, len(grid[0])))(pos):
        if pos2 not in rocks:
            yield cost, pos2


def reachable_by(distance_grid):
    maximum = max(c for row in distance_grid for c in row if c is not None)
    result = [0 for _ in range(maximum + 1)]
    for row in distance_grid:
        for c in row:
            if c is not None:
                result[c] += 1
    return result

def build_distance_list(start):
    distances = [[None for _ in row] for row in grid]
    def process(dist, pos):
        r, c = pos
        distances[r][c] = dist
    breadth_first(start, neighbors, process)
    raw_list = reachable_by(distances)
    return raw_list, (sum(raw_list[0::2]), sum(raw_list[1::2]))


df_n, wg_n = build_distance_list((0, startc))
df_ne, wg_ne = build_distance_list((0, len(grid[0])-1))
df_e, wg_e = build_distance_list((startr, len(grid[0])-1))
df_se, wg_se = build_distance_list((len(grid)-1, len(grid[0])-1))
df_s, wg_s = build_distance_list((len(grid)-1, startc))
df_sw, wg_sw = build_distance_list((len(grid)-1, 0))
df_w, wg_w = build_distance_list((startr, 0))
df_nw, wg_nw = build_distance_list((0, 0))
df_c, wg_c = build_distance_list(start)

def combine_lists(left, right):
    return list(map(operator.add, left, right))

# this is the part that assumes the grid is square and the start is in the center: we treat all straight directions
# and all diagonal directions as equivalent
df_straight = reduce(combine_lists, [df_n, df_e, df_s, df_w])
df_corner = reduce(combine_lists, [df_ne, df_se, df_sw, df_nw])
wg_straight = reduce(combine_lists, [wg_n, wg_e, wg_s, wg_w])
wg_corner = reduce(combine_lists, [wg_ne, wg_se, wg_sw, wg_nw])

# assume the initial grid is fully reachable
answer = wg_c[PART2_STEPS % 2]
# add the 1st, 3rd, &c full grids in straight directions from the center
answer += wg_straight[(PART2_STEPS + startr + 1) % 2] * ((full_grids + 1) // 2)
# add the 2nd, 4th, &c full grids in straight directions from the center (opposite parity because len(grid) is odd)
answer += wg_straight[(PART2_STEPS + startr) % 2] * (full_grids // 2)
# add the first incomplete grid in straight directions
answer += sum(df_straight[(PART2_STEPS + full_grids + startr + 1) % 2 : leftover_steps_straight + 1 : 2])
# if leftover steps reaches the far edge of the first incomplete grid but not the far corner, add the last incomplete grid
if leftover_steps_straight >= len(grid):
    answer += sum(df_straight[(PART2_STEPS + full_grids + startr) % 2 : leftover_steps_straight - len(grid) + 1 : 2])

# if the start grid is white, add all full white grids in diagonal directions
answer += wg_corner[(PART2_STEPS) % 2] * ((full_grids // 2) ** 2)
# add all black grids in diagonal directions
answer += wg_corner[(PART2_STEPS + 1) % 2] * (((full_grids - 1) // 2) ** 2 + (full_grids - 1) // 2)
# add first row of incomplete diagonal grids
answer += sum(df_corner[(PART2_STEPS + full_grids + 1) % 2 : leftover_steps_corner + len(grid) + 1 : 2]) * full_grids
if leftover_steps_corner >= 0:
    # add 2nd row of incomplete diagonal grids (it's possible we don't actually quite make it to this row)
    answer += sum(df_corner[(PART2_STEPS + full_grids) % 2 : leftover_steps_corner + 1 : 2]) * (full_grids + 1)


print(answer)
