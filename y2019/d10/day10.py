from math import gcd, atan2

with open("input.txt") as f:
    space = [line.strip() for line in f]

score = [[0 for x in line] for line in space]

def can_see(x1, y1, x2, y2):
    if space[y2][x2] == '.':
        return False
    if (x1, y1) == (x2, y2):
        return False
    count = gcd(x1-x2, y1-y2)
    dx = (x2-x1)//count
    dy = (y2-y1)//count
    for step in range(1, count):
        if space[y1 + step * dy][x1 + step * dx] == '#':
            return False
    return True


for y1 in range(len(space)):
    for x1 in range(len(space[y1])):
        if space[y1][x1] == '.':
            continue
        for y2 in range(len(space)):
            for x2 in range(len(space[y2])):
                if can_see(x1, y1, x2, y2):
                    score[y1][x1] = score[y1][x1] + 1

max_score, station_y, station_x = max((max((val, y, x) for x, val in enumerate(line))) for y, line in enumerate(score))
print(max_score, station_x, station_y)

# max_score > 200 so we don't need to worry about later passes
# collect all the zapped asteroids
victims = []
for y in range(len(space)):
    for x in range(len(space[y])):
        if space[y][x] == '.':
            continue
        if can_see(station_x, station_y, x, y):
            victims.append((x, y))

assert len(victims) == max_score

# for dx, dy in [(0, -2), (1, -2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (-1, 2), (-2, 2), (-2, 1), (-2, 0), (-2, -1), (-2, -2), (-1, -2)]:
#     print(dx, dy, -atan2(dx, dy))

# order by bearing
victims.sort(key=lambda p: -atan2(p[0] - station_x, p[1] - station_y))
print(victims[199])
