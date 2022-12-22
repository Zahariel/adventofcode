import parsing

WALL = '#'
EMPTY = '.'
SPACE = ' '

def parse(line):
    last_turn = -1
    result = []
    for i, c in enumerate(line):
        if c in {'L', 'R'}:
            result.append(int(line[last_turn+1:i]))
            result.append(c)
            last_turn = i
    result.append(int(line[last_turn+1:]))
    return result


def find_left(y):
    return min(map[y].index(EMPTY), map[y].index(WALL)), y

def find_right(y):
    return len(map[y]) - 1, y

def find_top(x):
    for i, line in enumerate(map):
        if x >= len(line) or line[x] == SPACE: continue
        return x, i

def find_bottom(x):
    for i, line in reversed(list(enumerate(map))):
        if x >= len(line) or line[x] == SPACE: continue
        return x, i

def resolve_coords(x, y, dx, dy):
    if y == 0 and dy < 0: return find_bottom(x)
    if y == len(map) - 1 and dy > 0: return find_top(x)
    if x == 0 and dx < 0: return find_right(y)
    if x == len(map[y]) - 1 and dx > 0: return find_left(y)
    tx, ty = x + dx, y + dy
    if tx >= len(map[ty]):
        if dy < 0: return find_bottom(tx)
        return find_top(tx)
    if map[ty][tx] == ' ':
        if dx < 0: return find_right(ty)
        if dy < 0: return find_bottom(tx)
        return find_top(tx)
    return tx, ty

def move(x, y, dx, dy, dist):
    for _ in range(dist):
        tx, ty = resolve_coords(x, y, dx, dy)
        if map[ty][tx] == WALL:
            break
        x, y = tx, ty
    return x, y

def print_map(x, y):
    for y2, line in enumerate(map):
        for x2, c in enumerate(line):
            if (x, y) == (x2, y2):
                print('@', end="")
            else:
                print(map[y2][x2], end="")
        print(y2)

DIR_VALUE = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}


# part 1

with open("input.txt") as file:
    raw_map, raw_instructions = tuple(parsing.split_on_blank(file))

    map = [line.rstrip() for line in raw_map]
    instructions = parse(raw_instructions[0])

print(instructions)

dx, dy = 1, 0
x, y = map[0].index(EMPTY), 0
print(x, y)

print_map(x, y)

for inst in instructions:
    if isinstance(inst, int):
        x, y = move(x, y, dx, dy, inst)
    elif inst == 'L':
        dx, dy = dy, -dx
    else:
        dx, dy = -dy, dx
    # print(inst, (x, y), (dx, dy))


print(1000 * (y+1) + 4 * (x+1) + DIR_VALUE[dx, dy])



# part 2
with open("input.txt") as file:
    raw_map, raw_instructions = tuple(parsing.split_on_blank(file))

    map = [line.rstrip() for line in raw_map]
    instructions = parse(raw_instructions[0])

# CUBE_SIZE = 4
# transitions = {
#     (1, 0): {
#         **{(3 * CUBE_SIZE - 1, y): (4 * CUBE_SIZE - 1, 3 * CUBE_SIZE - 1 - y, -1, 0) for y in range(CUBE_SIZE)},
#         **{(3 * CUBE_SIZE - 1, y + CUBE_SIZE): (4 * CUBE_SIZE - 1 - y, 2 * CUBE_SIZE, 0, 1) for y in range(CUBE_SIZE)},
#         **{(4 * CUBE_SIZE - 1, y + 2 * CUBE_SIZE): (3 * CUBE_SIZE - 1, CUBE_SIZE - 1 - y, -1, 0) for y in range(CUBE_SIZE)},
#     },
#     (0, 1): {
#         **{(x, 2 * CUBE_SIZE - 1): (3 * CUBE_SIZE - 1 - x, 3 * CUBE_SIZE - 1, 0, -1) for x in range(CUBE_SIZE)},
#         **{(x + CUBE_SIZE, 2 * CUBE_SIZE - 1): (2 * CUBE_SIZE, 3 * CUBE_SIZE - 1 - x, 1, 0) for x in range(CUBE_SIZE)},
#         **{(x + 2 * CUBE_SIZE, 3 * CUBE_SIZE - 1): (CUBE_SIZE - 1 - x, 2 * CUBE_SIZE - 1, 0, -1) for x in range(CUBE_SIZE)},
#         **{(x + 3 * CUBE_SIZE, 3 * CUBE_SIZE - 1): (0, 2 * CUBE_SIZE - 1 - x, 1, 0) for x in range(CUBE_SIZE)},
#     },
#     (-1, 0): {
#         **{(2 * CUBE_SIZE, y): (CUBE_SIZE + y, CUBE_SIZE, 0, 1) for y in range(CUBE_SIZE)},
#         **{(0, y + CUBE_SIZE): (4 * CUBE_SIZE - 1 - y, 3 * CUBE_SIZE - 1, 0, -1) for y in range(CUBE_SIZE)},
#         **{(2 * CUBE_SIZE, y + 2 * CUBE_SIZE): (2 * CUBE_SIZE - 1 - y, 2 * CUBE_SIZE - 1, -1, 0) for y in range(CUBE_SIZE)},
#     },
#     (0, -1): {
#         **{(x, CUBE_SIZE): (3 * CUBE_SIZE - 1 - x, 0, 0, 1) for x in range(CUBE_SIZE)},
#         **{(x + CUBE_SIZE, CUBE_SIZE): (2 * CUBE_SIZE, x, 1, 0) for x in range(CUBE_SIZE)},
#         **{(x + 2 * CUBE_SIZE, 0): (CUBE_SIZE - 1 - x, CUBE_SIZE, 0, 1) for x in range(CUBE_SIZE)},
#         **{(x + 3 * CUBE_SIZE, 2 * CUBE_SIZE): (3 * CUBE_SIZE - 1, 2 * CUBE_SIZE - 1 - x, -1, 0) for x in range(CUBE_SIZE)},
#     }
# }
CS = 50
transitions = {
    (1, 0): {
        **{(3 * CS - 1, y): (2 * CS - 1, 3 * CS - 1 - y, -1, 0) for y in range(CS)},
        **{(2 * CS - 1, y + CS): (2 * CS + y, CS - 1, 0, -1) for y in range(CS)},
        **{(2 * CS - 1, y + 2 * CS): (3 * CS - 1, CS - 1 - y, -1, 0) for y in range(CS)},
        **{(CS - 1, y + 3 * CS): (CS + y, 3 * CS - 1, 0, -1) for y in range(CS)},
    },
    (0, 1): {
        **{(x, 4 * CS - 1): (2 * CS + x, 0, 0, 1) for x in range(CS)},
        **{(x + CS, 3 * CS - 1): (CS - 1, 3 * CS + x, -1, 0) for x in range(CS)},
        **{(x + 2 * CS, CS - 1): (2 * CS - 1, CS + x, -1, 0) for x in range(CS)},
    },
    (-1, 0): {
        **{(CS, y): (0, 3 * CS - 1 - y, 1, 0) for y in range(CS)},
        **{(CS, y + CS): (y, 2 * CS, 0, 1) for y in range(CS)},
        **{(0, y + 2 * CS): (CS, CS - 1 - y, 1, 0) for y in range(CS)},
        **{(0, y + 3 * CS): (CS + y, 0, 0, 1) for y in range(CS)},
    },
    (0, -1): {
        **{(x, 2 * CS): (CS, CS + x, 1, 0) for x in range(CS)},
        **{(x + CS, 0): (0, 3 * CS + x, 1, 0) for x in range(CS)},
        **{(x + 2 * CS, 0): (x, 4 * CS - 1, 0, -1) for x in range(CS)},
    }
}

# sanity check
for dx, dy in transitions:
    for x, y in transitions[dx, dy]:
        tx, ty, tdx, tdy = transitions[dx,dy][x,y]
        assert transitions[-tdx, -tdy][tx, ty] == (x, y, -dx, -dy)

def cube_resolve_coords(x, y, dx, dy):
    tx, ty = x + dx, y + dy
    if ty >= 0 and ty < len(map) and tx >= 0 and tx < len(map[ty]) and map[ty][tx] != SPACE: return tx, ty, dx, dy
    return transitions[dx, dy][x, y]


def cube_move(x, y, dx, dy, dist):
    for _ in range(dist):
        tx, ty, tdx, tdy = cube_resolve_coords(x, y, dx, dy)
        if map[ty][tx] == WALL:
            break
        x, y, dx, dy = tx, ty, tdx, tdy
    return x, y, dx, dy


dx, dy = 1, 0
x, y = map[0].index(EMPTY), 0
print(x, y)

for inst in instructions:
    if isinstance(inst, int):
        x, y, dx, dy = cube_move(x, y, dx, dy, inst)
    elif inst == 'L':
        dx, dy = dy, -dx
    else:
        dx, dy = -dy, dx
    print(inst, (x, y), (dx, dy))

print(1000 * (y+1) + 4 * (x+1) + DIR_VALUE[dx, dy])
