import heapq

def breadth_first(start, neighbors_fn, process_fn):
    to_search = [(0, start)]
    heapq.heapify(to_search)
    seen = set()
    while len(to_search) > 0:
        dist, node = heapq.heappop(to_search)
        if node in seen:
            continue
        seen.add(node)
        result = process_fn(dist, node)
        if result is not None:
            return result
        for step, neighbor in neighbors_fn(node):
            heapq.heappush(to_search, (dist + step, neighbor))