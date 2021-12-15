import heapq

def breadth_first(start, neighbors_fn, process_fn, status=False):
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

# just a useful helper for constructing orthogonal neighbors in an n-dimensional grid
def ortho_neighbors(*bounds, cost_fn=(lambda c1,c2:1)):
    def neighbors(c):
        nbrs = []
        for dim in range(len(c)):
            if c[dim] > bounds[dim][0]:
                c2 = tuple(c[i] - 1 if i == dim else c[i] for i in range(len(c)))
                cost = cost_fn(c, c2)
                if cost is not None: nbrs.append((cost, c2))
            if c[dim] < bounds[dim][1] - 1:
                c2 = tuple(c[i] + 1 if i == dim else c[i] for i in range(len(c)))
                cost = cost_fn(c, c2)
                if cost is not None: nbrs.append((cost, c2))
        return nbrs

    return neighbors

