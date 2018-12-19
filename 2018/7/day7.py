import re
import heapq
from collections import defaultdict

def parse(line):
    match = re.match(r"Step (.) must be finished before step (.) can begin.", line.strip())
    return match.group(1), match.group(2)

def add_children_of(node, childrenOf, parentsOf, seen, queue):
    seen.add(node)
    if (node in childrenOf):
        for child in childrenOf[node]:
            if all(parent in seen for parent in parentsOf[child]):
                heapq.heappush(queue, child)

NUM_WORKERS = 5
DELAY_PER_STEP = 60
with open("day7input.txt") as file:
    edges = [parse(line) for line in file]
    childrenOf = defaultdict(set)
    parentsOf = defaultdict(set)
    for (parent, child) in edges:
        childrenOf[parent].add(child)
        parentsOf[child].add(parent)

    queue = [parent for (parent, child) in childrenOf.items() if parent not in parentsOf]
    heapq.heapify(queue)
    seen = set()
    while len(queue) > 0:
        node = heapq.heappop(queue)
        print(node, end="")
        add_children_of(node, childrenOf, parentsOf, seen, queue)
    print()

    queue = [parent for (parent, child) in childrenOf.items() if parent not in parentsOf]
    seen = set()
    time = 0
    workers = [(0, None) for i in range(NUM_WORKERS)]
    while len(queue) > 0 or any(a for (a,b) in workers):
        # schedule as many workers as possible
        while len(queue) > 0 and not all(a for (a, b) in workers):
            task = heapq.heappop(queue)
            cost = ord(task) - ord('A') + 1 + DELAY_PER_STEP
            worker = workers.index((0, None))
            workers[worker] = (cost, task)

        print(workers)
        # everyone ticks down one step
        for (i, (delay, task)) in enumerate(workers):
            if delay > 1:
                workers[i] = (delay-1, task)
            elif delay == 1:
                workers[i] = (0, None)
                add_children_of(task, childrenOf, parentsOf, seen, queue)
        time += 1
    print(time)