from coord_utils import in_bounds

CYCLE_COUNT = 1000000000

ROUND = 'O'
SQUARE = '#'
EMPTY = '.'

def parse(line):
    return list(line)

with open("input.txt") as file:
    grid = [parse(line.rstrip()) for line in file]

def tilt_one(original, result, r, c, dr, dc):
    cell = original[r][c]
    if cell == EMPTY: return
    if cell == SQUARE:
        result[r][c] = SQUARE
        return
    r2, c2 = r, c
    while in_bounds(result, r2, c2) and result[r2][c2] == EMPTY:
        r2 += dr
        c2 += dc
    result[r2-dr][c2-dc] = ROUND

def tilt(original, dr, dc):
    if dr < 0:
        row_iter = enumerate(original)
    else:
        row_iter = reversed(list(enumerate(original)))

    result = [[EMPTY for _ in row] for row in original]
    for r, row in row_iter:
        if dc < 0:
            column_iter = range(len(row))
        else:
            column_iter = reversed(range(len(row)))
        for c in column_iter:
            tilt_one(original, result, r, c, dr, dc)

    return result


def load_factor(grid):
    return sum(len(grid) - r for r, line in enumerate(grid) for cell in line if cell == ROUND)

def digest(grid):
    return "\n".join("".join(line) for line in grid)

print(load_factor(tilt(grid, -1, 0)))

def cycle(original):
    # tilt north
    northed = tilt(original, -1, 0)
    # tilt west
    wested = tilt(northed, 0, -1)
    # tilt south
    southed = tilt(wested, 1, 0)
    # tilt east
    easted = tilt(southed, 0, 1)

    return easted

MEMO = dict()

working = [[c for c in row] for row in grid]
repeat = None
for n in range(CYCLE_COUNT):
    if digest(working) in MEMO:
        repeat = n
        break
    else:
        MEMO[digest(working)] = n
    working = cycle(working)

cycle_length = repeat - MEMO[digest(working)]

# jump to last full repeat
last_repeat = (repeat - CYCLE_COUNT) % cycle_length + CYCLE_COUNT - cycle_length

# finish up last few cycles
for n in range(last_repeat, CYCLE_COUNT):
    working = cycle(working)

print(load_factor(working))
