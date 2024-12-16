from breadth_first import breadth_first, a_star
from dag import Dag
from utils import Coord2D


def parse(line):
    return [c for c in line]


with open("input.txt") as f:
    original_map = [parse(line.rstrip()) for line in f]

map = {Coord2D(x, y): cell for y, line in enumerate(original_map) for x, cell in enumerate(line)}

def find_symbol(symbol):
    for loc, cell in map.items():
        if cell == symbol:
            map[loc] = "."
            return loc

start = find_symbol("S")
end = find_symbol("E")

# start facing east
start_state = (start, Coord2D(1, 0))


def neighbors(state):
    point, dir = state
    next = point + dir
    if map[next] == ".":
        yield (1, (next, dir))
    right_turn = Coord2D(dir.y, -dir.x)
    yield (1000, (point, right_turn))
    yield (1000, (point, -right_turn))

def process(cost, state):
    point, _ = state
    if point == end:
        return cost

part1_result = breadth_first(start_state, neighbors_fn=neighbors, process_fn=process)
print(part1_result)


# part 2

approaches = dict()

def process2(prev, cost, state):
    if cost > part1_result: return True
    if prev is not None:
        approaches[state] = (cost, {prev})
    else:
        approaches[state] = (cost, set())

def revisit(prev, cost, state):
    old_cost, old_app = approaches[state]
    if cost == old_cost:
        old_app.add(prev)

a_star([start_state], neighbors_fn=neighbors, process_fn=process2, revisit_fn=revisit)

dag = Dag.from_children({node: apps for (node, (_, apps)) in approaches.items()})
results = dag.propagate_values({(end, Coord2D(0, -1)): True}, combiner=any)

print(len(set(loc for (loc, _), val in results.items() if val)))
