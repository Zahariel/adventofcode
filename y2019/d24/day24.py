
with open("input.txt") as f:
    initial_state = frozenset({(x, y) for y, line in enumerate(f) for x, c in enumerate(line) if c == '#'})

seen = set()
seen.add(initial_state)

def neighbors(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

def calc(state, pos, neighbors_fn):
    count = sum(1 for pos2 in neighbors_fn(*pos) if pos2 in state)
    return count == 1 or (count == 2 and pos not in state)

def generation(previous):
    return frozenset({(x, y) for x in range(5) for y in range(5) if calc(previous, (x, y), neighbors)})

state = initial_state
iters = 0
while True:
    state = generation(state)
    iters += 1
    if iters % 1000 == 0:
        print(iters)
    if state in seen:
        print("repeated state", iters, state)
        break
    seen.add(state)

def biodiversity(state):
    return sum(2 ** (x + 5 * y) for x, y in state)

print(biodiversity(state))



def rec_neighbors(x, y, z):
    # cells W
    if x == 0:
        yield 1, 2, z-1
    elif (x, y) == (3, 2):
        yield from ((4, i, z+1) for i in range(5))
    else:
        yield x-1, y, z

    # cells E
    if x == 4:
        yield 3, 2, z-1
    elif (x, y) == (1, 2):
        yield from ((0, i, z+1) for i in range(5))
    else:
        yield x+1, y, z

    # cells N
    if y == 0:
        yield 2, 1, z-1
    elif (x, y) == (2, 3):
        yield from ((i, 4, z+1) for i in range(5))
    else:
        yield x, y-1, z

    # cells S
    if y == 4:
        yield 2, 3, z-1
    elif (x, y) == (2, 1):
        yield from ((i, 0, z+1) for i in range(5))
    else:
        yield x, y+1, z

def rec_generation(state):
    min_z = min(z for _, _, z in state)
    max_z = max(z for _, _, z in state)
    return frozenset((x, y, z) for x in range(5) for y in range(5) for z in range(min_z - 1, max_z + 2) if (x, y) != (2, 2) and calc(state, (x, y, z), rec_neighbors))

rec_initial_state = frozenset((x, y, 0) for x, y in initial_state)
GENERATIONS = 200

print(rec_initial_state)

def print_rec_state(state):
    min_z = min(z for _, _, z in state)
    max_z = max(z for _, _, z in state)
    for z in range(min_z, max_z + 1):
        print("layer", z)
        for y in range(5):
            for x in range(5):
                if (x, y, z) in state:
                    print("#", end="")
                elif (x, y) == (2, 2):
                    print("?", end="")
                else:
                    print(".", end="")
            print()
        print()

state = rec_initial_state
for i in range(GENERATIONS):
    state = rec_generation(state)

print_rec_state(state)

print(len(state))
