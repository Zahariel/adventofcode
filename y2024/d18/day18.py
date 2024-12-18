import time

from parsy import string

from breadth_first import ortho_neighbors, breadth_first, a_star
from parsing import number
from utils import manhattan


def parse(line):
    return number.sep_by(string(",")).map(tuple).parse(line)

SIZE = 71

with open("input.txt") as f:
    bytes = [parse(line.rstrip()) for line in f]

active_bytes = set(bytes[:1024])

raw_neighbors = ortho_neighbors((0, SIZE), (0, SIZE))

def neighbors(point):
    return [(cost, nbr) for cost, nbr in raw_neighbors(point) if nbr not in active_bytes]

def process(cost, point):
    if point == (SIZE-1, SIZE-1):
        return cost

result = breadth_first((0, 0), neighbors_fn=neighbors, process_fn=process)

print(result)

# this takes about 20s
# for idx, new_byte in enumerate(bytes[1024:]):
#     active_bytes.add(new_byte)
#     result = a_star([(0, 0)], neighbors_fn=neighbors, process_fn=lambda _, c, p:process(c,p), estimator_fn=lambda p: manhattan(p, (SIZE-1, SIZE-1)))
#     if result is None:
#         print(",".join(str(coord) for coord in new_byte))
#         break
# active_bytes = set(bytes[:1024])


# alternate part 2 solution, only recheck if the previous shortest path got clobbered
# this is WAY faster, 560-580ms
start = time.perf_counter()
predecessor = dict()
def process2(prev, cost, point):
    predecessor[point] = prev
    if point == (SIZE-1, SIZE-1):
        return cost

def get_active_path():
    current = (SIZE-1, SIZE-1)
    result = {current}
    while current != (0, 0):
        current = predecessor[current]
        result.add(current)
    return result

result = a_star([(0, 0)], neighbors_fn=neighbors, process_fn=process2, estimator_fn=lambda p: manhattan(p, (SIZE-1, SIZE-1)))
path = get_active_path()

for new_byte in bytes[1024:]:
    active_bytes.add(new_byte)
    if new_byte not in path: continue
    result = a_star([(0, 0)], neighbors_fn=neighbors, process_fn=process2, estimator_fn=lambda p: manhattan(p, (SIZE-1, SIZE-1)))
    path = get_active_path()
    if result is None:
        print(f"{new_byte[0]},{new_byte[1]}")
        break
soln_1 = time.perf_counter()

# alternate part 2 solution 2, using binary search. 35-40ms, 15x faster than the previous solution!
lo = 1024
hi = len(bytes)
while lo + 1 < hi:
    mid = (lo + hi) // 2
    active_bytes = set(bytes[:mid])
    result = a_star([(0,0)], neighbors_fn=neighbors, process_fn=lambda _, c, p:process(c,p), estimator_fn=lambda p: manhattan(p, (SIZE-1, SIZE-1)))
    if result is None:
        hi = mid
    else:
        lo = mid

fail_byte = bytes[lo]
print(f"{fail_byte[0]},{fail_byte[1]}")

soln_2 = time.perf_counter()
print(soln_1 - start, soln_2 - soln_1)
