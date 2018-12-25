import re

def parse_line(line):
    x, y, z, t = re.match(r"(-?\d+),(-?\d+),(-?\d+),(-?\d+)", line).groups()
    return int(x), int(y), int(z), int(t)

def find(parents, x):
    while parents[x] != x:
        x, parents[x] = parents[x], parents[parents[x]]
    return x

def union(parents, ranks, x1, x2):
    x1 = find(parents, x1)
    x2 = find(parents, x2)
    if x1 == x2: return
    if ranks[x1] < ranks[x2]: x1, x2 = x2, x1
    parents[x2] = x1
    if ranks[x1] == ranks[x2]: ranks[x1] += 1

def manhattan(p1, p2):
    x1, y1, z1, t1 = p1
    x2, y2, z2, t2 = p2
    if x1 < x2: x1, x2 = x2, x1
    if y1 < y2: y1, y2 = y2, y1
    if z1 < z2: z1, z2 = z2, z1
    if t1 < t2: t1, t2 = t2, t1
    return x1 - x2 + y1 - y2 + z1 - z2 + t1 - t2

with open("day25input.txt") as file:
    points = [parse_line(line) for line in file]

parents = [i for i in range(len(points))]
ranks = [0 for _ in points]

RANGE = 3
for i, p1 in enumerate(points):
    for j, p2 in enumerate(points[:i]):
        d = manhattan(p1, p2)
        if d <= RANGE:
            union(parents, ranks, i, j)

print(sum(1 for i,p in enumerate(parents) if i == p))
