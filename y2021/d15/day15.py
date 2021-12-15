import breadth_first

def parse(line):
    return [int(c) for c in line.strip()]

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

TARGET = (len(data[0]) - 1, len(data) - 1)

def neighbors(c):
    x, y = c
    nbrs = []
    if x > 0: nbrs.append((data[y][x-1], (x-1, y)))
    if x < len(data[y]) - 1: nbrs.append((data[y][x+1], (x+1, y)))
    if y > 0: nbrs.append((data[y-1][x], (x, y-1)))
    if y < len(data) - 1: nbrs.append((data[y+1][x], (x, y+1)))
    return nbrs

def visit(dist, c):
    if c == TARGET: return dist
    return None

result = breadth_first.breadth_first((0,0), neighbors_fn=neighbors, process_fn=visit)
print(result)

# part 2
REPEATS = 5
TARGET2 = (len(data[0]) * REPEATS - 1, len(data) * REPEATS - 1)

def get_threat(x, y):
    big_x = x // len(data[0])
    small_x = x % len(data[0])
    big_y = y // len(data)
    small_y = y % len(data)
    return (data[small_y][small_x] + big_x + big_y - 1) % 9 + 1

def neighbors2(c):
    x, y = c
    nbrs = []
    if x > 0: nbrs.append((get_threat(x-1, y), (x-1, y)))
    if x < len(data[0]) * REPEATS - 1: nbrs.append((get_threat(x+1, y), (x+1, y)))
    if y > 0: nbrs.append((get_threat(x, y-1), (x, y-1)))
    if y < len(data) * REPEATS - 1: nbrs.append((get_threat(x, y+1), (x, y+1)))
    return nbrs

def visit2(dist, c):
    if c == TARGET2: return dist
    return None

result = breadth_first.breadth_first((0,0), neighbors_fn=neighbors2, process_fn=visit2)
print(result)
