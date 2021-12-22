import re
from collections import defaultdict

def parse(line):
    action, xmin, xmax, ymin, ymax, zmin, zmax = re.match(r"(\S+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line.strip()).groups()
    return (action == "on"), int(xmin), int(xmax)+1, int(ymin), int(ymax)+1, int(zmin), int(zmax)+1

with open("input.txt") as f:
    data = [parse(line) for line in f.readlines()]


# part 1
reactor = defaultdict(bool)
INIT_LIMIT = 50

for action, xmin, xmax, ymin, ymax, zmin, zmax in data:
    if not (-INIT_LIMIT <= xmin <= INIT_LIMIT): break
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            for z in range(zmin, zmax):
                reactor[x,y,z] = action

print(sum(1 if c else 0 for c in reactor.values()))

# part 2
# that's not going to work this time

class Cuboid:
    def __init__(self, action, xmin, xmax, ymin, ymax, zmin, zmax):
        self.action = action
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

    def intersection(self, other):
        if not (
            self.xmin < other.xmax and
            other.xmin < self.xmax and
            self.ymin < other.ymax and
            other.ymin < self.ymax and
            self.zmin < other.zmax and
            other.zmin < self.zmax
        ): return None
        return Cuboid(self.action,
                      max(self.xmin, other.xmin), min(self.xmax, other.xmax),
                      max(self.ymin, other.ymin), min(self.ymax, other.ymax),
                      max(self.zmin, other.zmin), min(self.zmax, other.zmax))

    def volume(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin) * (self.zmax - self.zmin)

    def __repr__(self):
        return f"Cuboid({self.action},{self.xmin},{self.xmax},{self.ymin},{self.ymax},{self.zmin},{self.zmax})"

data = [Cuboid(*vals) for vals in data]

tiers = defaultdict(list)

for cuboid in data:
    print(f"processing {cuboid}")
    for tier in sorted(tiers, reverse=True):
        for other in tiers[tier]:
            intersection = cuboid.intersection(other)
            if intersection:
                tiers[tier+1].append(intersection)
    if cuboid.action:
        tiers[0].append(cuboid)
        # just don't include the basic volume of "off" cuboids, that's the only difference

volume = 0
for tier, cuboids in tiers.items():
    volume += ((-1) ** tier) * sum(cuboid.volume() for cuboid in cuboids)

print(volume)
