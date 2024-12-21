import itertools
from collections import Counter

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
}


#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

directional_keypad = {
    "^": Coord2D(1, 0),
    "A": Coord2D(2, 0),
    "<": Coord2D(0, 1),
    "v": Coord2D(1, 1),
    ">": Coord2D(2, 1),
}

MOVE_BUTTONS = {
    Coord2D(0, 1): "v",
    Coord2D(-1, 0): "<",
    Coord2D(0, -1): "^",
    Coord2D(1, 0): ">",
}

def horiz_moves(current, target):
    if current.x < target.x:
        return ">" * (target.x - current.x)
    else:
        return "<" * (current.x - target.x)

def vert_moves(current, target):
    if current.y < target.y:
        return "v" * (target.y - current.y)
    else:
        return "^" * (current.y - target.y)

def numerical_robot(output):
    results = [""]
    for current, target in itertools.pairwise("A" + output):
        c = numeric_keypad[current]
        t = numeric_keypad[target]
        # avoid 0, 3
        if c.y == 3 and t.x == 0:
            results = [result + vert_moves(c, t) + horiz_moves(c, t) for result in results]
        elif c.x == 0 and t.y == 3:
            results = [result + horiz_moves(c, t) + vert_moves(c, t) for result in results]
        else:
            results = [*(result + vert_moves(c, t) + horiz_moves(c, t) for result in results),
                       *(result + horiz_moves(c, t) + vert_moves(c, t) for result in results)]
        results = [result + "A" for result in results]
    return results

raw_best_paths = {
    ("A", "A"): "A",
    ("A", "^"): "<A",
    ("A", "<"): "v<<A",
    ("A", ">"): "vA",
    ("A", "v"): "<vA",
    ("^", "A"): ">A",
    ("^", "^"): "A",
    ("^", "<"): "v<A",
    ("^", ">"): "v>A",
    ("^", "v"): "vA",
    ("<", "A"): ">>^A",
    ("<", "^"): ">^A",
    ("<", "<"): "A",
    ("<", ">"): ">>A",
    ("<", "v"): ">A",
    (">", "A"): "^A",
    (">", "^"): "<^A",
    (">", "<"): "<<A",
    (">", ">"): "A",
    (">", "v"): "<A",
    ("v", "A"): ">^A",
    ("v", "^"): "^A",
    ("v", "<"): "<A",
    ("v", ">"): ">A",
    ("v", "v"): "A",
}

best_paths = {trans: (path[0], Counter(itertools.pairwise(path))) for trans, path in raw_best_paths.items()}

def input_for_output(start, output_map):
    input_map = Counter()
    first_input, first_path = best_paths["A", start]
    input_map.update(first_path)
    for output_trans, count in output_map.items():
        first, moves = best_paths[output_trans]
        input_map["A", first] += count
        for input_trans, amt in moves.items():
            input_map[input_trans] += amt * count
    return first_input, input_map

def find_best(output, robots):
    raw_numerical_moves = numerical_robot(output)
    possibilities = [(seq[0], Counter(itertools.pairwise(seq))) for seq in raw_numerical_moves]
    for i in range(robots - 1):
        possibilities = [input_for_output(*p) for p in possibilities]
    return min(sum(moves.values()) + 1 for _, moves in possibilities)

def complexity(output, robots):
    min_input = find_best(output, robots)
    print(output, min_input)
    numeric_part = int(output[:-1])
    return min_input * numeric_part

# this works for part 1 but not part 2 and i'm not sure why, i assume it has to do with the shortcuts inherent in
# raw_best_paths but i'm not sure how to fix that without a really big exponential explosion

print(sum(complexity(output, 3) for output in lines))

print(sum(complexity(output, 26) for output in lines))


