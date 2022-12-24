from breadth_first import breadth_first
from keyeddefaultdict import KeyedDefaultdict

def parse(line):
    return line

with open("input.txt") as file:
    map = [parse(line.rstrip()) for line in file]

EMPTY = '.'
WALL = '#'


H_BLIZZARDS = {
    '<': -1,
    '>': 1,
}

V_BLIZZARDS = {
    '^': -1,
    'v': 1,
}

x = map[0].index(EMPTY)
y = 0

def move_h_blizzard(x0, y0, dx, t):
    modulus = len(map[0]) - 2
    return (x0 + dx * t - 1) % modulus + 1, y0

def move_v_blizzard(x0, y0, dy, t):
    modulus = len(map) - 2
    return x0, (y0 + dy * t - 1) % modulus + 1

def calc_blizzards(t):
    result = set()
    for y, line in enumerate(map):
        for x, c in enumerate(line):
            if c in H_BLIZZARDS:
                result.add(move_h_blizzard(x, y, H_BLIZZARDS[c], t))
            if c in V_BLIZZARDS:
                result.add(move_v_blizzard(x, y, V_BLIZZARDS[c], t))
    return result

blizzards = KeyedDefaultdict(calc_blizzards)

def neighbors(c):
    t, x, y = c
    for target in [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        if map[y][x] == WALL: continue
        if target in blizzards[t+1]: continue
        yield 1, (t+1, *target)

def process(t, c):
    t2, x, y = c
    assert t == t2
    if y == len(map) - 1 and map[y][x] == EMPTY: return t
    return None

time = breadth_first((0, x, y), neighbors_fn=neighbors, process_fn=process)

print(time)

def neighbors2(c):
    t, phase, x, y = c
    if phase == 1 and y == len(map) - 1 and map[y][x] == EMPTY: yield 0, (t, 2, x, y)
    if phase == 2 and y == 0 and map[y][x] == EMPTY: yield 0, (t, 3, x, y)
    for (x2, y2) in [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        if y2 < 0 or y2 >= len(map): continue
        if map[y][x] == WALL: continue
        if (x2, y2) in blizzards[t+1]: continue
        yield 1, (t+1, phase, x2, y2)

def process2(t, c):
    t2, phase, x, y = c
    assert t == t2
    if phase == 3 and y == len(map) - 1 and map[y][x] == EMPTY: return t
    return None

time = breadth_first((0, 1, x, y), neighbors_fn=neighbors2, process_fn=process2)
print(time)
