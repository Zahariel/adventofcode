from parsy import seq, string

from breadth_first import ortho_neighbors, flood_fill
from parsing import number
from utils import Coord2D


def parse(line):
    return seq(
        seq(string("p=") >> number,
                    string(",") >> number).map(lambda l: Coord2D(*l)),
        seq(string(" v=") >> number,
            string(",") >> number).map(lambda l: Coord2D(*l))
    ).map(tuple).parse(line)


FILE = "input.txt"
WIDTH = 101
HEIGHT = 103

# FILE = "test.txt"
# WIDTH = 11
# HEIGHT = 7

with open(FILE) as f:
    robots = [parse(line.rstrip()) for line in f]

STEPS = 100
def walk_around(time):
    def wrap(coord):
        x, y = coord
        return Coord2D(x % WIDTH, y % HEIGHT)

    return [wrap(start + time * v) for start, v in robots]

step1_robots = walk_around(STEPS)

NW = sum(1 for x, y in step1_robots if x < WIDTH//2 and y < HEIGHT//2)
NE = sum(1 for x, y in step1_robots if x > WIDTH//2 and y < HEIGHT//2)
SW = sum(1 for x, y in step1_robots if x < WIDTH//2 and y > HEIGHT//2)
SE = sum(1 for x, y in step1_robots if x > WIDTH//2 and y > HEIGHT//2)

print(NW * NE * SW * SE)

# part 2???

def inspect(time):
    snapshot = walk_around(time)
    snapshot_set = set(snapshot)
    needs_check = set(snapshot_set)
    # look for a big solid group
    while needs_check:
        start = needs_check.pop()
        block = flood_fill(start, neighbors_fn=ortho_neighbors((0, WIDTH), (0, HEIGHT)), include_fn=snapshot_set.__contains__)
        needs_check -= block
        if len(block) >= 200:
            # this is a candidate
            print(i)
            for r in range(HEIGHT):
                print("".join("*" if (c, r) in snapshot_set else "." for c in range(WIDTH)))
            print(i)
            input()

for i in range(10000):
    if i % 500 == 0: print(i)
    inspect(i)

# the answer was 6493


