from breadth_first import breadth_first
from coord_utils import in_bounds

def parse(line):
    return [int(c) for c in line]

with open("input.txt") as file:
    grid = [parse(line.rstrip()) for line in file]


DIRS = {
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
}

def make_neighbors(min_dist, max_dist):
    def neighbors(state):
        r, c, dr, dc = state
        possible_dirs = set(DIRS)

        if (dr, dc) in possible_dirs:
            possible_dirs.remove((dr, dc))
            possible_dirs.remove((-dr, -dc))
        for (dr2, dc2) in possible_dirs:
            total_cost = 0
            for dist in range(1, max_dist):
                r2, c2 = r + dr2 * dist, c + dc2 * dist
                if in_bounds(grid, r2, c2):
                    total_cost += grid[r2][c2]
                    if dist < min_dist: continue
                    yield (total_cost, (r2, c2, dr2, dc2))

    return neighbors


def check_state(dist, state):
    r, c, _, _ = state
    if r == len(grid)-1 and c == len(grid[-1]) - 1:
        return dist


cost = breadth_first((0, 0, 0, 0), make_neighbors(1, 4), check_state)
print(cost)

ultra_cost = breadth_first((0, 0, 0, 0), make_neighbors(4, 11), check_state)
print(ultra_cost)

