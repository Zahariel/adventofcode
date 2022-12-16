import re
from collections import defaultdict

from breadth_first import breadth_first

def parse(line):
    [name, rate, connections] = re.match(r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line).groups()
    return name, int(rate), [conn.strip() for conn in connections.split(",")]

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

valves = {valve[0]: valve for valve in lines}

travel = defaultdict(lambda: defaultdict(int))

for name in valves:
    _, rate, connections = valves[name]

    def record(dist, n):
        travel[name][n] = dist

    breadth_first(name, neighbors_fn=lambda n: [(1, n2) for n2 in valves[n][2]], process_fn=record)

print(travel)

useful_valves = set(valve for (valve, rate, _) in valves.values() if rate > 0)
print(useful_valves)

def wander(current_path, remaining, time_left, released, best_so_far, best_path):
    # print(current_path, remaining, time_left, released, best_so_far, best_path)
    if best_so_far is not None and released + time_left * sum(valves[name][1] for name in remaining) < best_so_far:
        # can't do better
        return best_so_far, best_path

    if best_so_far is None or released > best_so_far:
        # we can always stop here
        best_so_far = released
        best_path = current_path

    for name in remaining:
        new_time = time_left - travel[current_path[-1]][name] - 1
        if new_time < 0: continue
        new_remaining = set(remaining)
        new_remaining.remove(name)
        new_released = released + valves[name][1] * new_time
        new_path = list(current_path)
        new_path.append(name)
        best_so_far, best_path = wander(new_path, new_remaining, new_time, new_released, best_so_far, best_path)

    return best_so_far, best_path

best, best_path = wander(['AA'], useful_valves, 30, 0, None, None)
print(best, best_path)

# part 2

def dual_wander(current_me, me_time_left, current_elephant, elephant_time_left, remaining, released, best_so_far):
    # print(current_me, me_time_left, current_elephant, elephant_time_left, remaining, released, best_so_far)
    old_best = best_so_far
    if released + max(me_time_left, elephant_time_left) * sum(valves[name][1] for name in remaining) < best_so_far:
        return best_so_far
    if released > best_so_far:
        # can always stop here
        best_so_far = released

    for name in remaining:
        new_remaining = set(remaining)
        new_remaining.remove(name)
        new_time_me = me_time_left - travel[current_me][name] - 1
        if new_time_me > 0:
            new_released = released + valves[name][1] * new_time_me
            best_so_far = dual_wander(name, new_time_me, current_elephant, elephant_time_left, new_remaining, new_released, best_so_far)
        new_time_ele = elephant_time_left - travel[current_elephant][name] - 1
        if new_time_ele > 0:
            new_released = released + valves[name][1] * new_time_ele
            best_so_far = dual_wander(current_me, me_time_left, name, new_time_ele, new_remaining, new_released, best_so_far)

    if best_so_far > old_best:
        print(best_so_far)
    return best_so_far

best = dual_wander('AA', 26, 'AA', 26, useful_valves, 0, 0)
print("really best", best)
