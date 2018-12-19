import re
import heapq
def parse(line):
    match = re.match(r"(\d+), (\d+)", line)
    return int(match.group(1)), int(match.group(2))

def manhattan(first, second):
    (x1, y1), (x2, y2) = first, second
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    return (x2 - x1) + (y2 - y1)

def closest(points, probe):
    dists = [(manhattan(point, probe), point) for point in points]
    heapq.heapify(dists)
    first = heapq.heappop(dists)
    second = heapq.heappop(dists)
    if first[0] == second[0]: return None
    return first[1]

def neighbors(point):
    (x,y) = point
    yield (x+1, y)
    yield (x-1, y)
    yield (x, y+1)
    yield (x, y-1)

def floodgrow(start, max, func):
    queue = [(0, start)]
    seen = set()
    while len(seen) < max and len(queue) > 0:
        (dist, point) = heapq.heappop(queue)
        if point in seen: continue
        if func(point):
            seen.add(point)
            for neighbor in neighbors(point):
                if neighbor not in seen:
                    heapq.heappush(queue, (dist + 1, neighbor))
    return len(seen) if len(seen) < max else -1

def calcsize(points, seed):
    return floodgrow(seed, 10000, lambda probe: closest(points, probe) == seed)

MAX_DIST = 10000
with open("day6input.txt") as file:
    points = [parse(line.strip()) for line in file]

    sizes = [(calcsize(points, point), point) for point in points]
    print(max(sizes))

    center = (int(sum(x for (x,y) in points)/len(points)), int(sum(y for (x,y) in points)/len(points)))
    print(floodgrow(center, 100000, lambda probe: sum(manhattan(probe, point) for point in points) < MAX_DIST))

