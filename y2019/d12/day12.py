import re
from math import gcd
from functools import reduce

class Moon():
    def __init__(self, line):
        line = line.strip()
        x, y, z = re.match("<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line).groups()
        self.coords = [int(x), int(y), int(z)]
        self.vel = [0, 0, 0]

    def gravity(self, other):
        for i in range(3):
            if self.coords[i] < other.coords[i]:
                self.vel[i] = self.vel[i] + 1
            elif self.coords[i] > other.coords[i]:
                self.vel[i] = self.vel[i] - 1

    def move(self):
        for i in range(3):
            self.coords[i] = self.coords[i] + self.vel[i]

    def kinetic(self):
        return sum(abs(x) for x in self.vel)

    def potential(self):
        return sum(abs(x) for x in self.coords)

    def energy(self):
        return self.potential() * self.kinetic()

with open("input.txt") as f:
    moons = [Moon(line) for line in f]

TIME = 1000

def step(moons):
    for left in moons:
        for right in moons:
            if left == right:
                continue
            left.gravity(right)
    for moon in moons:
        moon.move()

for t in range(TIME):
    step(moons)

print(sum(moon.energy() for moon in moons))

# reset
with open("input.txt") as f:
    initial_moons = [Moon(line) for line in f]
with open("input.txt") as f:
    moons = [Moon(line) for line in f]

t = 0
matches = dict()
while len(matches) < 3:
    step(moons)
    t = t + 1
    if t % 1_000_000 == 0:
        print(t)
    for d in range(3):
        if d not in matches:
            if all(moons[i].vel[d] == 0 and moons[i].coords[d] == initial_moons[i].coords[d] for i in range(4)):
                print("found", d, "at", t)
                matches[d] = t

def lcm(a, b):
    return (a * b) // gcd(a, b)

print(matches)
print(reduce(lcm, matches.values()))

