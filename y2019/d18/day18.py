from breadth_first import breadth_first

with open("input.txt") as f:
    map = [line.strip() for line in f]

allkeys = set()

start_x, start_y = 0, 0
for y, row in enumerate(map):
    for x, cell in enumerate(row):
        if cell == '@':
            start_x, start_y = x, y
        elif cell in 'qwertyuiopasdfghjklzxcvbnm':
            allkeys.add(cell)

def neighbors(state):
    x, y, keys = state
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        newx, newy = x + dx, y + dy
        if newx < 0 or newx >= len(map[0]):
            continue
        if newy < 0 or newy >= len(map):
            continue
        cell = map[newy][newx]
        if cell == '#':
            continue
        if cell in 'QWERTYUIOPASDFGHJKLZXCVBNM' and cell.lower() not in keys:
            continue
        if cell in 'qwertyuiopasdfghjklzxcvbnm':
            yield 1, (newx, newy, keys | set(cell))
        else:
            yield 1, (newx, newy, keys)

def done(dist, state):
    x, y, keys = state
    if keys == allkeys:
        return dist
    else:
        return None

# dist = breadth_first((start_x, start_y, frozenset()), neighbors, done)
# print(dist)


with open("input_altered.txt") as f:
    map = [line.strip() for line in f]

allkeys = set()

starts = tuple()
for y, row in enumerate(map):
    for x, cell in enumerate(row):
        if cell == '@':
            starts = starts + ((x, y),)
        elif cell in 'qwertyuiopasdfghjklzxcvbnm':
            allkeys.add(cell)

def multineighbors(state):
    locs, keys = state

    def explore(c):
        x, y = c
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            newx, newy = x + dx, y + dy
            if newx < 0 or newx >= len(map[0]):
                continue
            if newy < 0 or newy >= len(map):
                continue
            cell = map[newy][newx]
            if cell == '#':
                continue
            if cell in 'QWERTYUIOPASDFGHJKLZXCVBNM' and cell.lower() not in keys:
                continue
            yield 1, (newx, newy)


    for i, (bot_x, bot_y) in enumerate(locs):
        found_keys = dict()
        def findkey(dist, c):
            x, y = c
            cell = map[y][x]
            if cell in 'qwertyuiopasdfghjklzxcvbnm' and cell not in keys and (x, y) not in found_keys:
                found_keys[x, y] = dist
        # get keys
        breadth_first((bot_x, bot_y), explore, findkey)
        for (newx, newy), dist in found_keys.items():
            yield dist, (tuple(locs[:i] + ((newx, newy),) + locs[i+1:]), keys | set(map[newy][newx]))

def multidone(dist, state):
    locs, keys = state
    if keys == allkeys:
        return dist
    else:
        return None

dist = breadth_first((starts, frozenset()), multineighbors, multidone, status=True)
print(dist)
