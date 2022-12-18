import breadth_first

def parse(line):
    return tuple(int(c) for c in line.split(","))

with open("input.txt") as file:
    drops = [parse(line.rstrip()) for line in file]

drops = set(drops)
# print(drops)


def neighbors(x, y, z):
    yield (x-1, y, z)
    yield (x+1, y, z)
    yield (x, y-1, z)
    yield (x, y+1, z)
    yield (x, y, z-1)
    yield (x, y, z+1)

def surface(drops):
    surface = 0
    for x, y, z in drops:
        surface += 6
        for c2 in neighbors(x, y, z):
            if c2 in drops:
                surface -= 1
    return surface

full_surface = surface(drops)
print(full_surface)

# part 2
max_x = max(x for (x, _, _) in drops)
max_y = max(y for (_, y, _) in drops)
max_z = max(z for (_, _, z) in drops)

print(max_x, max_y, max_z)

interior = set((x, y, z) for x in range(-1, max_x + 1) for y in range(-1, max_y + 1) for z in range(-1, max_z + 1))
interior.difference_update(drops)

def flood_neighbors(c):
    return [(1, c2) for c2 in neighbors(*c) if c2 in interior]

def process(_, c):
    interior.remove(c)

breadth_first.breadth_first((-1, -1, -1), neighbors_fn=flood_neighbors, process_fn=process)

interior_surface = surface(interior)
print("interior", interior_surface)
print(full_surface - interior_surface)
