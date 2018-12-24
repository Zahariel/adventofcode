import re
import z3

def parse_line(line):
    x, y, z, r = re.match(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line).groups()
    return int(r), (int(x), int(y), int(z))

with open("day23input.txt") as file:
    bots = [parse_line(line) for line in file]

def zdist(x1, x2):
    return z3.If(x1 < x2, x2 - x1, x1 - x2)

def zmanhattan(x1, y1, z1, x2, y2, z2):
    return zdist(x1, x2) + zdist(y1, y2) + zdist(z1, z2)

x, y, z, from_zero = z3.Ints("x y z from_zero")
solver = z3.Optimize()

for r, (x1, y1, z1) in bots:
    solver.add_soft(zmanhattan(x, y, z, x1, y1, z1) <= r)

solver.add(from_zero == zmanhattan(x, y, z, 0, 0, 0))
solver.minimize(from_zero)

print(solver.check())
print(solver.model())
# print(solver.objectives())