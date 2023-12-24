import itertools
import math

import z3
from parsy import seq, string, whitespace

from parsing import number
from utils import Coord3D

INPUT_FILE = "input.txt"
TEST_MIN = 200000000000000
TEST_MAX = 400000000000000

def parse(line):

    coord = number.sep_by(string(",") >> whitespace, min=3, max=3).map(lambda l : Coord3D(*l))
    parser = seq(
        coord,
        whitespace >> string("@") >> whitespace >> coord
    ).map(tuple)
    return parser.parse(line)




with open(INPUT_FILE) as file:
    hailstones = [parse(line.rstrip()) for line in file]


def in_test_area(coords, parameters):
    return all(TEST_MIN <= coord <= TEST_MAX for coord in coords) and all(p >= 0 for p in parameters)

def collide_2d(stone1, stone2):
    (x1, y1, _), (vx1, vy1, _) = stone1
    (x2, y2, _), (vx2, vy2, _) = stone2

    disc = vx1 * vy2 - vy1 * vx2
    if disc == 0:
        return (0, 0), (-math.inf, -math.inf)
    t = (vx2 * (y1 - y2) - vy2 * (x1 - x2)) / disc
    u = (vx1 * (y1 - y2) - vy1 * (x1 - x2)) / disc

    xc = x1 + t * vx1
    yc = y1 + t * vy1
    return (xc, yc), (t, u)


collisions = 0
for stone1, stone2 in itertools.combinations(hailstones, 2):
    collision = collide_2d(stone1, stone2)
    if in_test_area(*collision):
        collisions += 1

print(collisions)


# part 2 oh wow
# i tried several different ways to do this without z3 and none of them worked
solver = z3.Solver()

px, py, pz, vx, vy, vz, s, t, u = z3.Ints("px py pz vx vy vz s t u")

# i need 3 hailstones so i have 9 equations in 9 unknowns
p1, v1 = hailstones[0]
p2, v2 = hailstones[1]
p3, v3 = hailstones[2]

# i bet this doesn't matter but just to help z3 out a little
solver.add(s > 0)
solver.add(t > 0)
solver.add(u > 0)

def add_equations(stone_p, stone_v, time):
    solver.add(px + vx * time == stone_p.x + stone_v.x * time)
    solver.add(py + vy * time == stone_p.y + stone_v.y * time)
    solver.add(pz + vz * time == stone_p.z + stone_v.z * time)

add_equations(p1, v1, s)
add_equations(p2, v2, t)
add_equations(p3, v3, u)

solver.check()
model = solver.model()

print(model.eval(px + py + pz))
