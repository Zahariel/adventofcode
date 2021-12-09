import breadth_first

def parse(line):
    return [int(c) for c in line.strip()]

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

def neighbors(grid, i, j):
    neighbors = []
    if i > 0:
        neighbors.append((i-1, j))
    if i < len(grid) - 1:
        neighbors.append((i+1, j))
    if j > 0:
        neighbors.append((i, j-1))
    if j < len(grid[i]) - 1:
        neighbors.append((i, j+1))
    return neighbors

risk = 0
low_points = []
for i, row in enumerate(data):
    for j, cell in enumerate(row):
        if all(data[i2][j2] > cell for i2,j2 in neighbors(data, i, j)):
            risk += cell + 1
            low_points.append((i, j))
print(risk)

# part 2
def floodfill(grid, i, j):
    count = 0
    def process(dist, c):
        nonlocal count
        count += 1
        return None

    def bf_neighbors(node):
        nbrs = neighbors(grid, node[0], node[1])
        return [(1, (i2, j2)) for i2, j2 in nbrs if grid[i2][j2] < 9]

    breadth_first.breadth_first((i, j), bf_neighbors, process)
    return count

basins = [floodfill(data, i, j) for i, j in low_points]
basins = sorted(basins)
print(basins[-1] * basins[-2] * basins[-3])


