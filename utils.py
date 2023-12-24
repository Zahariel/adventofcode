import math
import operator
from typing import NamedTuple

def manhattan(coords1, coords2):
    return sum(abs(x - y) for (x, y) in zip(coords1, coords2))


def chinese_remainder(equations):
    lcm = math.lcm(*(modulus for _, modulus in equations))


    inverses = [pow(modulus, -1, lcm//modulus) for _, modulus in equations]

    return sum(residue * inv * (lcm // modulus) for (residue, modulus), inv in zip(equations, inverses)) % lcm, lcm

def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[r])

def coord_add(coords1, coords2):
    return tuple(map(operator.add, coords1, coords2))


class Coord3D(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Coord3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Coord3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Coord3D(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return Coord3D(other * self.x, other * self.y, other * self.x)

    def __truediv__(self, other):
        return Coord3D(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other):
        return Coord3D(self.x // other, self.y // other, self.z // other)
