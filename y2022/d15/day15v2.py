import re

import z3

from coord_utils import manhattan


class Sensor():
    def __init__(self, s_x, s_y, b_x, b_y):
        self.x = s_x
        self.y = s_y
        self.beacon_x = b_x
        self.beacon_y = b_y
        self.range = manhattan((s_x, s_y), (b_x, b_y))

    def __repr__(self):
        return f"Sensor({self.x}, {self.y}, {self.beacon_x}, {self.beacon_y})"

def parse(line):
    [s_x, s_y, b_x, b_y] = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line).groups()
    return Sensor(int(s_x), int(s_y), int(b_x), int(b_y))

with open("input.txt") as file:
    sensors = [parse(line.rstrip()) for line in file]

LIMIT = 4000000

s = z3.Solver()

x, y = z3.Ints("x y")

s.add(x >= 0)
s.add(x <= LIMIT)
s.add(y >= 0)
s.add(y <= LIMIT)

def z3abs(x):
    return z3.If(x < 0, -x, x)

for sensor in sensors:
    s.add(z3abs(sensor.x - x) + z3abs(sensor.y - y) > sensor.range)

print(s.check())
m = s.model()
print(m.eval(x), m.eval(y), m.eval(x * 4000000 + y))
