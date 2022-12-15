import re
import portion

from utils import manhattan

class Sensor():
    def __init__(self, s_x, s_y, b_x, b_y):
        self.x = s_x
        self.y = s_y
        self.beacon_x = b_x
        self.beacon_y = b_y
        self.range = manhattan((s_x, s_y), (b_x, b_y))

    def __repr__(self):
        return f"Sensor({self.x}, {self.y}, {self.beacon_x}, {self.beacon_y})"

    def find_sensed_portion(self, y):
        vert = abs(self.y - y)
        if vert > self.range:
            return portion.empty()
        return portion.closedopen(self.x - (self.range - vert), self.x + (self.range - vert) + 1)

def parse(line):
    [s_x, s_y, b_x, b_y] = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line).groups()
    return Sensor(int(s_x), int(s_y), int(b_x), int(b_y))

with open("input.txt") as file:
    sensors = [parse(line.rstrip()) for line in file]

TEST_Y = 2000000
UPPER_BOUND = 4000000

# TEST_Y = 10
# UPPER_BOUND = 20

print(sensors)

all_sensors = set((s.x, s.y) for s in sensors)
all_beacons = set((s.beacon_x, s.beacon_y) for s in sensors)

def build_exclusion(test_y):
    acc = portion.empty()
    for s in sensors:
        acc = acc | s.find_sensed_portion(test_y)
    return acc

acc = build_exclusion(TEST_Y)
for (x, y) in all_beacons:
    if y == TEST_Y:
        acc = acc - portion.closedopen(x, x+1)

print(acc)
impossible_len = sum(part.upper - part.lower for part in acc)
print(impossible_len)

# part 2
allowed = portion.closed(0, UPPER_BOUND)
for i in range(UPPER_BOUND + 1):
    if i % 100000 == 0:
        print("working", i)
    possible = allowed - build_exclusion(i)
    if possible != portion.empty():
        print(possible, i)
        print((possible.lower + 1) * 4000000 + i)
        break
