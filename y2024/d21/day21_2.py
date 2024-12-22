import functools
import itertools

from utils import Coord2D


def parse(line):
    return line


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

numeric_keypad = {
    "1": Coord2D(0, 2),
    "2": Coord2D(1, 2),
    "3": Coord2D(2, 2),
    "4": Coord2D(0, 1),
    "5": Coord2D(1, 1),
    "6": Coord2D(2, 1),
    "7": Coord2D(0, 0),
    "8": Coord2D(1, 0),
    "9": Coord2D(2, 0),
    "0": Coord2D(1, 3),
    "A": Coord2D(2, 3),
    "avoid": Coord2D(0, 3)
}

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
directional_keypad = {
    "avoid": Coord2D(0, 0),
    "^": Coord2D(1, 0),
    "A": Coord2D(2, 0),
    "<": Coord2D(0, 1),
    "v": Coord2D(1, 1),
    ">": Coord2D(2, 1),
}

move_buttons = {
    Coord2D(-1, 0): "<",
    Coord2D(0, 1): "v",
    Coord2D(1, 0): ">",
    Coord2D(0, -1): "^",
}

def horiz_moves(start, end):
    if start.x < end.x:
        return ">" * (end.x - start.x)
    else:
        return "<" * (start.x - end.x)

def vert_moves(start, end):
    if start.y < end.y:
        return "v" * (end.y - start.y)
    else:
        return "^" * (start.y - end.y)

def build_paths(keypad, start, end):
    s = keypad[start]
    e = keypad[end]
    avoid = keypad["avoid"]
    result = []
    if not(s.x == avoid.x and e.y == avoid.y):
        result.append(vert_moves(s, e) + horiz_moves(s, e) + "A")
    if not(s.y == avoid.y and e.x == avoid.x):
        result.append(horiz_moves(s, e) + vert_moves(s, e) + "A")
    return result

@functools.cache
def calc_length(output, expansions, numeric):
    if expansions == 0:
        return len(output)
    result = 0
    for start, end in itertools.pairwise("A" + output):
        paths = build_paths(numeric_keypad if numeric else directional_keypad, start, end)
        costs = [calc_length(path, expansions-1, False) for path in paths]
        result += min(costs)
    return result

def complexity(output, expansions):
    return int(output[:-1]) * calc_length(output, expansions, True)

print(sum(complexity(line, 3) for line in lines))

print(sum(complexity(line, 26) for line in lines))
