import breadth_first

def parse(line):
    return [int(c) for c in line.strip()]

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

neighbors = breadth_first.ortho_neighbors((0, len(data)), (0, len(data[0])))

risk = 0
low_points = []
for i, row in enumerate(data):
    for j, cell in enumerate(row):
        if all(data[i2][j2] > cell for _,(i2,j2) in neighbors((i, j))):
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

    bf_neighbors = breadth_first.ortho_neighbors((0, len(data)), (0, len(data[0])), cost_fn=lambda _,c: 1 if grid[c[0]][c[1]] < 9 else None)

    breadth_first.breadth_first((i, j), bf_neighbors, process)
    return count

basins = [floodfill(data, i, j) for i, j in low_points]
basins = sorted(basins)
print(basins[-1] * basins[-2] * basins[-3])


