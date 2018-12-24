import re
import z3

def parse_line(line):
    x, y, z, r = re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line).groups()
    return int(r), (int(x), int(y), int(z))

def manhattan(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    if x1 > x2: x1, x2 = x2, x1
    if y1 > y2: y1, y2 = y2, y1
    if z1 > z2: z1, z2 = z2, z1
    return x2 - x1 + y2 - y1 + z2 - z1

with open("day23input.txt") as file:
    bots = [parse_line(line) for line in file]

max_r, max_pos = max(bots)
print(sum(1 for (_, pos) in bots if manhattan(pos, max_pos) <= max_r))

def zdist(x1, x2):
    return z3.If(x1 < x2, x2 - x1, x1 - x2)

def zmanhattan(x1, y1, z1, x2, y2, z2):
    return zdist(x1, x2) + zdist(y1, y2) + zdist(z1, z2)

x, y, z, num_in_range, from_zero = z3.Ints("x y z num_in_range from_zero")
solver = z3.Optimize()
in_range = []
for r, (x1, y1, z1) in bots:
    in_range.append(z3.If(zmanhattan(x, y, z, x1, y1, z1) <= r, 1, 0))
solver.add(num_in_range == z3.Sum(in_range))
solver.add(from_zero == zmanhattan(x, y, z, 0, 0, 0))
solver.maximize(num_in_range)
solver.minimize(from_zero)

print(solver.check())
print(solver.model())

