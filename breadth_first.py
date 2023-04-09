import heapq
from collections.abc import Iterable, Sequence
from typing import Optional, TypeVar, Callable

STATE = TypeVar("STATE")
RESULT = TypeVar("RESULT")

def breadth_first(start:STATE, neighbors_fn:Callable[[STATE], Iterable[tuple[int, STATE]]], process_fn:Callable[[int, STATE], Optional[RESULT]], status:bool=False) -> Optional[RESULT]:
    to_search = [(0, start)]
    heapq.heapify(to_search)
    seen = set()
    current_dist = 0
    while len(to_search) > 0:
        dist, node = heapq.heappop(to_search)
        if status and dist > current_dist:
            print(dist)
            current_dist = dist
        if node in seen:
            continue
        seen.add(node)
        result = process_fn(dist, node)
        if result is not None:
            return result
        for step, neighbor in neighbors_fn(node):
            heapq.heappush(to_search, (dist + step, neighbor))
    return None

COORD = TypeVar("COORD", bound=Sequence[int])
# just a useful helper for constructing orthogonal neighbors in an n-dimensional grid
def ortho_neighbors(*bounds:tuple[int, int], cost_fn:Callable[[COORD, COORD], Optional[int]]=(lambda c1,c2:1)) -> Callable[[COORD], list[tuple[int, COORD]]]:
    def neighbors(c):
        nbrs = []
        for dim in range(len(c)):
            lo, hi = bounds[dim]
            if c[dim] > lo:
                c2 = tuple(c[i] - 1 if i == dim else c[i] for i in range(len(c)))
                cost = cost_fn(c, c2)
                if cost is not None: nbrs.append((cost, c2))
            if c[dim] < hi - 1:
                c2 = tuple(c[i] + 1 if i == dim else c[i] for i in range(len(c)))
                cost = cost_fn(c, c2)
                if cost is not None: nbrs.append((cost, c2))
        return nbrs

    return neighbors

