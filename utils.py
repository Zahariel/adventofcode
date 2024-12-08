import math
import operator
from typing import NamedTuple, TypeVar


def manhattan(coords1, coords2):
    return sum(abs(x - y) for (x, y) in zip(coords1, coords2))


def chinese_remainder(equations):
    lcm = math.lcm(*(modulus for _, modulus in equations))


    inverses = [pow(modulus, -1, lcm//modulus) for _, modulus in equations]

    return sum(residue * inv * (lcm // modulus) for (residue, modulus), inv in zip(equations, inverses)) % lcm, lcm

def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[r])

CoordType = TypeVar("CoordType", bound=tuple[int | float, ...])
def coord_add(coords1:CoordType, coords2:CoordType) -> CoordType:
    return tuple(map(operator.add, coords1, coords2))
def coord_sub(coords1:CoordType, coords2:CoordType) -> CoordType:
    return tuple(map(operator.sub, coords1, coords2))
def coord_scale(coords:CoordType, scale:int|float) -> CoordType:
    return tuple(map(lambda x: x * scale, coords))


# note: this is an infinite ray, hope you know what you're doing
def coord_vector(start, dir):
    while True:
        yield start
        start = coord_add(start, dir)

ORTHO_DIRS = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
]

DIAG_DIRS = [
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1),
]

class Coord2D(NamedTuple):
    x: int
    y: int

    def ray(self, dir):
        start = self
        while True:
            yield start
            start = start + dir

    def __add__(self, other):
        return Coord2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Coord2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Coord2D(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Coord2D(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Coord2D(self.x // other, self.y // other)

    def __neg__(self):
        return Coord2D(-self.x, -self.y)

class Coord3D(NamedTuple):
    x: int
    y: int
    z: int

    def ray(self, dir):
        start = self
        while True:
            yield start
            start = start + dir


    def __add__(self, other):
        return Coord3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Coord3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Coord3D(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return Coord3D(other * self.x, other * self.y, other * self.z)

    def __truediv__(self, other):
        return Coord3D(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other):
        return Coord3D(self.x // other, self.y // other, self.z // other)

    def __neg__(self):
        return Coord3D(-self.x, -self.y, -self.z)
