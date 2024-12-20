from breadth_first import ortho_neighbors, breadth_first
from utils import Coord2D, manhattan, find_and_replace_symbol


def parse(line):
    return list(line)


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

map = {
    Coord2D(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)
}

start = find_and_replace_symbol(map, "S", ".")
end = find_and_replace_symbol(map, "E", ".")
raw_neighbors = ortho_neighbors((0, len(lines[0])), (0, len(lines)))

def neighbors(loc):
    return [(cost, nbr) for cost, nbr in raw_neighbors(loc) if map[nbr] != "#"]

from_start = dict()
from_end = dict()

def process_forward(cost, loc):
    from_start[loc] = cost
    if loc == end:
        return cost

def process_backward(cost, loc):
    from_end[loc] = cost
    if loc == start:
        return cost

base_cost = breadth_first(start, neighbors_fn=neighbors, process_fn=process_forward)
breadth_first(end, neighbors_fn=neighbors, process_fn=process_backward)

def check_cheat(enter, leave):
    if enter in from_start and leave in from_end:
        return base_cost - (from_start[enter] + from_end[leave] + manhattan(enter, leave))

# part 1
MAX_CHEAT = 2
small_savings = {(enter, enter + Coord2D(dx, dy)): check_cheat(enter, enter + Coord2D(dx, dy)) for enter in map for dx in range(-MAX_CHEAT, MAX_CHEAT+1) for dy in range(-(MAX_CHEAT - abs(dx)), (MAX_CHEAT - abs(dx))+1)}
small_savings = {coords: saved for coords, saved in small_savings.items() if saved is not None}
print(sum(1 for s in small_savings.values() if s >= 100))

# part 2, this takes kind of a while
MAX_CHEAT = 20
big_savings = {(enter, enter + Coord2D(dx, dy)): check_cheat(enter, enter + Coord2D(dx, dy)) for enter in map for dx in range(-MAX_CHEAT, MAX_CHEAT+1) for dy in range(-(MAX_CHEAT - abs(dx)), (MAX_CHEAT - abs(dx))+1)}
big_savings = {coords: saved for coords, saved in big_savings.items() if saved is not None and saved > 0}
print(sum(1 for s in big_savings.values() if s >= 100))
