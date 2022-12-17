

jet_dir = {
    '>': 1,
    '<': -1,
}

with open("input.txt") as file:
    jets = [jet_dir[c] for c in file.readline().rstrip()]

rocks = [
    [(2, 0), (3, 0), (4, 0), (5, 0)],
    [(2, 1), (3, 1), (4, 1), (3, 0), (3, 2)],
    [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)],
    [(2, 0), (2, 1), (2, 2), (2, 3)],
    [(2, 0), (3, 0), (2, 1), (3, 1)],
]

MAX_ROCKS = 2022
# MAX_ROCKS = 10000
WIDTH = 7
arena = set()
for x in range(WIDTH):
    arena.add((x, -1))


def print_arena(lines=-1, offset=0, top=-1):
    if top < 0:
        top = max(y for (_, y) in arena)
    bottom = top - lines if lines > 0 else -1
    for y in range(top, bottom, -1):
        row = "".join("#" if (x, y) in arena else "." for x in range(WIDTH))
        print(f"|{row}| {y + offset}")
    print("=" * (WIDTH + 2))
    print()

next_rock = 0
def get_rock():
    global next_rock
    top = max(y for (_, y) in arena)
    result = [(x, y + top + 4) for (x, y) in rocks[next_rock]]
    next_rock += 1
    next_rock %= len(rocks)
    return result

rock = get_rock()

def blast_rock(dir):
    global rock
    if any(x + dir < 0 for (x, _) in rock): return
    if any(x + dir >= WIDTH for (x, _) in rock): return
    if any((x + dir, y) in arena for (x, y) in rock): return
    rock = [(x+dir, y) for (x, y) in rock]

def drop_rock():
    global rock
    global arena
    if any((x, y-1) in arena for (x, y) in rock):
        spot = min(x for (x, _) in rock)
        arena.update(rock)
        rock = get_rock()
        return spot
    else:
        rock = [(x, y-1) for (x, y) in rock]
        return None

rock_count = 0
while rock_count < MAX_ROCKS:
    for blast in jets:
        blast_rock(blast)
        if drop_rock() is not None:
            # print_arena()
            rock_count += 1
            if rock_count == MAX_ROCKS:
                break

print(max(y for (_, y) in arena) + 1)
print_arena(10)

# part 2
# i really should have seen this coming

# wind index, upcoming rock, tower top -> rock count, height
memory = dict()
arena = set()
for x in range(WIDTH):
    arena.add((x, -1))

next_rock = 0
rock = get_rock()
rock_count = 0
MAX_ROCKS = 1000000000000
offset = 0
LOOKBACK = 20
while rock_count < MAX_ROCKS:
    for idx, blast in enumerate(jets):
        blast_rock(blast)
        stopped = drop_rock()
        if stopped is not None:
            rock_count += 1
            if rock_count >= MAX_ROCKS: break
            # look in memory
            if offset != 0:
                # already found cycle, just trying to get the last few done
                continue

            height = max(y for (_, y) in arena)
            tower_top = frozenset((x, y - height) for (x, y) in arena if y > height - LOOKBACK)
            if (idx, next_rock, tower_top) in memory:
                old_rock, old_height = memory[idx, next_rock, tower_top]
                print("repeat found", (idx, next_rock, stopped), (old_rock, old_height), (rock_count, height))
                height_diff = height - old_height
                rocks_diff = rock_count - old_rock
                additional_cycles = (MAX_ROCKS - rock_count) // rocks_diff
                offset = height_diff * additional_cycles
                rock_count += rocks_diff * additional_cycles
                print(rocks_diff, height_diff, additional_cycles, offset, rock_count)
                print_arena(20)
                print_arena(20, 0, old_height)
            else:
                memory[idx, next_rock, tower_top] = (rock_count, height)

height = max(y for (_, y) in arena)
print(rock_count, height + 1)

print(height + offset + 1)
print_arena(10, offset)
