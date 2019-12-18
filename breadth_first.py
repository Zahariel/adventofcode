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
