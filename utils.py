def manhattan(coords1, coords2):
    return sum(abs(x - y) for (x, y) in zip(coords1, coords2))
