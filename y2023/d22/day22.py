from typing import Optional

from parsy import seq, string

from parsing import number

class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = tuple(c+1 for c in end)
        self.supporters = set()
        self.supported = set()

    def __repr__(self):
        return f"Brick({self.start}-{self.end} -> {len(self.supporters)}, {len(self.supported)})"

    def footprint(self):
        return ((r, c) for r in range(self.start[0], self.end[0]) for c in range(self.start[1], self.end[1]))


def parse(line):
    coord = number.sep_by(string(","), min=3, max=3).map(tuple)
    parser = seq(
        coord << string("~"),
        coord
    ).map(tuple)
    return Brick(*parser.parse(line))

with open("input.txt") as file:
    bricks = [parse(line.rstrip()) for line in file]


# all x and y are 0-9
MAPSIZE = 10
heightmap:list[list[tuple[int, Optional[Brick]]]] = [[(0, None) for _ in range(MAPSIZE)] for _ in range(MAPSIZE)]

sorted_bricks = list(sorted(bricks, key=lambda b: b.start[2]))

def drop_brick(brick):
    landing_height = max(heightmap[r][c][0] for r, c in brick.footprint())
    top = landing_height + (brick.end[2] - brick.start[2])
    for r, c in brick.footprint():
        if heightmap[r][c][0] == landing_height and heightmap[r][c][1] is not None:
            brick.supporters.add(heightmap[r][c][1])
            heightmap[r][c][1].supported.add(brick)
        heightmap[r][c] = (top, brick)

for i, brick in enumerate(sorted_bricks):
    drop_brick(brick)

print(sum(0 if any(len(b2.supporters) == 1 for b2 in b.supported) else 1 for b in sorted_bricks))


def vaporize(brick):
    gone = {brick}
    wobbly = set(brick.supported)
    while len(wobbly) > 0:
        target = wobbly.pop()
        if target.supporters <= gone:
            gone.add(target)
            wobbly.update(target.supported)
    return gone

total = 0
for vaporized in sorted_bricks:
    total += len(vaporize(vaporized)) - 1

print(total)
