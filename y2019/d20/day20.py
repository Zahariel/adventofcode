from collections import defaultdict
from breadth_first import breadth_first

with open("input.txt") as f:
    maze = [l.strip("\n") for l in f]
    bottom_edge = len(maze) - 3
    right_edge = len(maze[2]) - 3

PORTAL_TAGS = set('QWERTYUIOPASDFGHJKLZXCVBNM')

portals = defaultdict(list)
for y, line in enumerate(maze):
    # don't need edges
    if y == 0 or y == len(maze) - 1:
        continue
    for x, cell in enumerate(line):
        if x == 0 or x == len(line) - 1:
            continue

        if cell in PORTAL_TAGS:
            # figure out full name
            portal_name = None
            entrance_x, entrance_y = -1, -1
            for dx, dy, reverse in [(1, 0, True), (0, 1, True), (-1, 0, False), (0, -1, False)]:
                entrance = maze[y + dy][x + dx]
                if entrance == '.':
                    portal_name = (maze[y-dy][x-dx] + maze[y][x]) if reverse else (maze[y][x] + maze[y-dy][x-dx])
                    entrance_x, entrance_y = x + dx, y + dy
                    break

            if entrance_x < 0:
                continue

            portals[portal_name].append((entrance_x, entrance_y))

start_x, start_y = portals.pop("AA")[0]
end_x, end_y = portals.pop("ZZ")[0]

teleports = dict()
for ends in portals.values():
    teleports[ends[0]] = ends[1]
    teleports[ends[1]] = ends[0]

print(teleports)

def neighbors(c):
    x, y = c
    if (x, y) in teleports:
        yield 1, teleports[x, y]
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if maze[y+dy][x+dx] == '.':
            yield 1, (x+dx, y+dy)

def check(dist, c):
    if c == (end_x, end_y):
        return dist
    return None

result = breadth_first((start_x, start_y), neighbors, check)
print(result)


def rec_neighbors(c):
    x, y, level = c
    if (x, y) in teleports:
        # figure out whether to go up or down
        t_x, t_y = teleports[x, y]
        if x == 2 or x == right_edge or y == 2 or y == bottom_edge:
            # outward portal
            if level > 0:
                yield 1, (t_x, t_y, level - 1)
        else:
            # inward portal
            yield 1, (t_x, t_y, level + 1)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if maze[y+dy][x+dx] == '.':
            yield 1, (x+dx, y+dy, level)

def rec_check(dist, c):
    if c == (end_x, end_y, 0):
        return dist
    return None

rec_result = breadth_first((start_x, start_y, 0), rec_neighbors, rec_check)
print(rec_result)
