from collections import defaultdict
from functools import cache

from coord_utils import coord_add, in_bounds


def parse(line):
    return [c for c in line]

with open("input.txt") as file:
    grid = [parse(line.rstrip()) for line in file]

PATH = '.'
FOREST = '#'
SLOPES = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0),
}


# this assumes that all fork and join points are protected by slopes
start = (0, 1)
end = (len(grid) - 1, len(grid[-1]) - 2)

distances = dict()
distances[start] = 0

stack = [((1, 1), start)]

forks = {start, end}

def neighbors(r, c):
    return {(r+dr, c+dc) for (dr, dc) in SLOPES.values() if in_bounds(grid, r+dr, c+dc) and grid[r+dr][c+dc] != FOREST}

while len(stack) > 0:
    here, prev = stack.pop()
    nbrs = neighbors(*here)
    if len(nbrs) <= 2:
        # just follow the path
        nbrs.remove(prev)
        distances[here] = distances[prev] + 1
        stack.extend((nbr, here) for nbr in nbrs)
    else:
        forks.add(here)
        inputs = {(nr, nc) for (nr, nc) in nbrs if here == coord_add((nr, nc), SLOPES[grid[nr][nc]])}
        outputs = nbrs - inputs
        if all(i in distances and distances[i] is not None for i in inputs):
            # we can process this square
            distance = max(distances[nbr] for nbr in inputs) + 1
            distances[here] = distance
            stack.extend((nbr, here) for nbr in outputs)
        else:
            # we can't do anything with this node right now, we'll find it again
            pass

print(distances[end])



# part 2, so much for my assumption

# build graph of fork points
path_neighbors = defaultdict(dict)
stack = [((1, 1), 1, start, start)]

while len(stack) > 0:
    here, dist, prev, begin = stack.pop()
    nbrs = neighbors(*here)
    nbrs.remove(prev)
    if here not in forks:
        # just follow the path
        stack.append((nbrs.pop(), dist+1, here, begin))
    else:
        if begin not in path_neighbors[here]:
            # close this path
            path_neighbors[begin][here] = dist
            path_neighbors[here][begin] = dist
            # start new paths
            stack.extend((nbr, 1, here, here) for nbr in nbrs)


@cache
def exhaustive_search(node, visited):
    if node == end:
        return 0
    longest = 0
    new_visited = frozenset(visited | {node})
    for next in (path_neighbors[node].keys() - visited):
        result = exhaustive_search(next, new_visited) + path_neighbors[node][next]
        if result > longest:
            longest = result
    return longest

print(exhaustive_search(start, frozenset()))
