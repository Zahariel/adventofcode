import heapq
from collections.abc import Iterable, Sequence
from typing import Callable, NamedTuple, Optional, TypeVar

STATE = TypeVar("STATE")
RESULT = TypeVar("RESULT")

def breadth_first(
        start:STATE,
        neighbors_fn:Callable[[STATE], Iterable[tuple[int, STATE]]],
        process_fn:Callable[[int, STATE], Optional[RESULT]] = (lambda _, __: None),
        status:bool=False
) -> Optional[RESULT]:
    return a_star([start], neighbors_fn, process_fn, lambda _: 0, status)

def breadth_first_multiple_starts(
        starts:Iterable[STATE],
        neighbors_fn:Callable[[STATE], Iterable[tuple[int, STATE]]],
        process_fn:Callable[[int, STATE], Optional[RESULT]] = (lambda _, __: None),
        status:bool=False
) -> Optional[RESULT]:
    return a_star(starts, neighbors_fn, process_fn, lambda _: 0, status)

class Node[STATE](NamedTuple):
    est: int
    dist: int
    state: STATE

    def __lt__(self, other):
        return (self.est, self.dist) < (other.est, other.dist)


def a_star(
        starts:Iterable[STATE],
        neighbors_fn:Callable[[STATE], Iterable[tuple[int, STATE]]],
        process_fn:Callable[[int, STATE], Optional[RESULT]] = (lambda _, __: None),
        estimator_fn:Callable[[STATE], int] = lambda _: 0,
        status:bool=False
) -> Optional[RESULT]:
    to_search = [Node(estimator_fn(start), 0, start) for start in starts]
    heapq.heapify(to_search)
    seen = set()
    current_est = 0
    while len(to_search) > 0:
        est, dist, state = heapq.heappop(to_search)
        if status and est > current_est:
            print(dist, est)
            current_est = est
        if state in seen:
            continue
        seen.add(state)
        result = process_fn(dist, state)
        if result is not None:
            return result
        for step, neighbor in neighbors_fn(state):
            heapq.heappush(to_search, Node(dist + step + estimator_fn(neighbor), dist + step, neighbor))
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

# it seems like I use this a lot so I'm turning it into a utility
def flood_fill(start:STATE, neighbors_fn:Callable[[STATE], Iterable[tuple[int, STATE]]], include_fn:Callable[[STATE], bool]) -> set[STATE]:
    result = set()
    def real_neighbors(state):
        return [(cost, nbr) for (cost, nbr) in neighbors_fn(state) if include_fn(nbr)]
    def process(_, state):
        result.add(state)
    breadth_first(start, neighbors_fn=real_neighbors, process_fn=process)
    return result
