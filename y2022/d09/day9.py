DIRS = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}

def parse(line):
    dir, dist = line.split()
    return DIRS[dir], int(dist)

with open("input.txt") as file:
    moves = [parse(line.rstrip()) for line in file]

head_x, head_y = 0, 0
tail_x, tail_y = 0, 0

tail_visited = set()

def resolve_tail(tail_x, tail_y, head_x, head_y):
    x_dist = head_x - tail_x
    y_dist = head_y - tail_y
    dx = int(x_dist / 2)
    dy = int(y_dist / 2)

    tail_x += dx
    tail_y += dy
    if dx != 0 and dy == 0:
        # move y anyway
        tail_y = head_y
    if dy != 0 and dx == 0:
        # move x anyway
        tail_x = head_x

    return tail_x, tail_y

for (dx, dy), dist in moves:
    for i in range(dist):
        head_x += dx
        head_y += dy
        tail_x, tail_y = resolve_tail(tail_x, tail_y, head_x, head_y)
        tail_visited.add((tail_x, tail_y))

print(tail_visited)
print(len(tail_visited))

# part 2
KNOTS = 10
rope = [(0,0)] * KNOTS
tail_visited = set()

for (dx, dy), dist in moves:
    for _ in range(dist):
        head_x, head_y = rope[0]
        head_x += dx
        head_y += dy
        rope[0] = (head_x, head_y)
        for k in range(1, KNOTS):
            rope[k] = resolve_tail(*rope[k], *rope[k-1])
        tail_visited.add(rope[-1])

print(tail_visited)
print(len(tail_visited))
