import operator
from functools import reduce

from breadth_first import ortho_neighbors
from dag import Dag


def parse(line):
    return [int(c) for c in line]

with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

grid = {(r, c): h for r, line in enumerate(lines) for c, h in enumerate(line)}

HEIGHT = len(lines)
WIDTH = len(lines[0])
RAW_NEIGHBORS = ortho_neighbors((0, HEIGHT), (0, WIDTH))

move_edges = [(point, nbr) for point, h in grid.items() for _, nbr in RAW_NEIGHBORS(point) if grid[nbr] == h + 1]

dag = Dag.from_child_edges(move_edges)

trailheads = [point for point, h in grid.items() if h == 0]

initial_reachable = {h: {h} for h in trailheads}
reachable = dag.propagate_values(initial_reachable, lambda vs: reduce(operator.or_, vs, set()))
print(sum(len(x) for point, x in reachable.items() if grid[point] == 9))

initial_paths = {h: 1 for h in trailheads}
paths = dag.propagate_values(initial_paths, sum)
print(sum(x for point, x in paths.items() if grid[point] == 9))
