from collections import defaultdict

from breadth_first import ortho_neighbors, breadth_first


def parse(line):
    return [int(c) for c in line]


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

grid = {(r, c): h for r, line in enumerate(lines) for c, h in enumerate(line)}

HEIGHT = len(lines)
WIDTH = len(lines[0])
RAW_NEIGHBORS = ortho_neighbors((0, HEIGHT), (0, WIDTH))


trailheads = [point for point, h in grid.items() if h == 0]

def score(head):
    total = 0
    def neighbors(point):
        return [(cost, nbr) for cost, nbr in RAW_NEIGHBORS(point) if grid[nbr] == grid[point] + 1]
    def process(_, point):
        nonlocal total
        if grid[point] == 9:
            total += 1
    breadth_first(head, neighbors_fn=neighbors, process_fn=process)
    return total

print(sum(score(head) for head in trailheads))

# part 2

def rating(head):
    paths = defaultdict(int)
    paths[head] = 1
    total = 0
    def neighbors(point):
        for cost, nbr in RAW_NEIGHBORS(point):
            if grid[nbr] == grid[point] + 1:
                paths[nbr] += paths[point]
                yield cost, nbr
    def process(_, point):
        nonlocal total
        if grid[point] == 9:
            total += paths[point]
    breadth_first(head, neighbors_fn=neighbors, process_fn=process)
    return total

print(sum(rating(head) for head in trailheads))
