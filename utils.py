import math
import operator
from typing import Dict

from typing import NamedTuple, TypeVar



def chinese_remainder(equations):
    """Solves x = r1 (mod m1); x = r2 (mod m2); ... given (r1, m1), (r2, m2), ...
    Returns x, M = lcm(m1, m2, ...)"""
    lcm = math.lcm(*(modulus for _, modulus in equations))


    inverses = [pow(modulus, -1, lcm//modulus) for _, modulus in equations]

    return sum(residue * inv * (lcm // modulus) for (residue, modulus), inv in zip(equations, inverses)) % lcm, lcm

def solve_diophantine(a, b):
    """Solves a * s + b * t = gcd(a, b) = r"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r > 0:
        q = old_r // r
        old_r, r = r, old_r % r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_s, old_t, old_r




def manhattan(coords1, coords2):
    return sum(abs(x - y) for (x, y) in zip(coords1, coords2))

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

ORTHO_DIRS = [
    Coord2D(0, 1),
    Coord2D(1, 0),
    Coord2D(0, -1),
    Coord2D(-1, 0),
]

DIAG_DIRS = [
    Coord2D(1, 1),
    Coord2D(-1, 1),
    Coord2D(-1, -1),
    Coord2D(1, -1),
]

KEY = TypeVar("KEY")
VALUE = TypeVar("VALUE")
def find_and_replace_symbol(start: Dict[KEY, VALUE], symbol: VALUE, replacement: VALUE) -> KEY:
    for loc, cell in start.items():
        if cell == symbol:
            start[loc] = replacement
            return loc
