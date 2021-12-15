import breadth_first

def parse(line):
    return [int(c) for c in line.strip()]

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

TARGET = (len(data[0]) - 1, len(data) - 1)

neighbors = breadth_first.ortho_neighbors((0, TARGET[0] + 1), (0, TARGET[1] + 1), cost_fn=lambda _,c: data[c[0]][c[1]])

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

neighbors2 = breadth_first.ortho_neighbors((0, TARGET2[0] + 1), (0, TARGET2[1] + 1), cost_fn=lambda _,c: get_threat(*c))

def visit2(dist, c):
    if c == TARGET2: return dist
    return None

result = breadth_first.breadth_first((0,0), neighbors_fn=neighbors2, process_fn=visit2)
print(result)
