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

raw_paths = {
    ("A", "A"): ["A"],
    ("A", "^"): ["<A"],
    ("A", "<"): ["v<<A"],
    ("A", ">"): ["vA"],
    ("A", "v"): ["<vA", "v<A"],
    ("^", "A"): [">A"],
    ("^", "^"): ["A"],
    ("^", "<"): ["v<A"],
    ("^", ">"): ["v>A", ">vA"],
    ("^", "v"): ["vA"],
    ("<", "A"): [">>^A"],
    ("<", "^"): [">^A"],
    ("<", "<"): ["A"],
    ("<", ">"): [">>A"],
    ("<", "v"): [">A"],
    (">", "A"): ["^A"],
    (">", "^"): ["<^A", "^<A"],
    (">", "<"): ["<<A"],
    (">", ">"): ["A"],
    (">", "v"): ["<A"],
    ("v", "A"): [">^A", "^>A"],
    ("v", "^"): ["^A"],
    ("v", "<"): ["<A"],
    ("v", ">"): [">A"],
    ("v", "v"): ["A"],
}

path_maps = {trans: [(path[0], Counter(itertools.pairwise(path))) for path in paths] for trans, paths in raw_paths.items()}

def input_for_output(start, output_map):
    first_paths = path_maps["A", start]
    possibilities = [(start, Counter(moves)) for start, moves in first_paths]
    for output_trans, count in output_map.items():
        next_possibilities = []
        for output_start, output_moves in path_maps[output_trans]:
            for start, moves in possibilities:
                updated:Counter[tuple[str, str]] = Counter(moves)
                updated["A", output_start] += count
                for input_trans, amt in output_moves.items():
                    updated[input_trans] += amt * count
                next_possibilities.append((start, updated))
        possibilities = next_possibilities
    return possibilities

def find_best(output, robots):
    raw_numerical_moves = numerical_robot(output)
    possibilities = [(seq[0], Counter(itertools.pairwise(seq))) for seq in raw_numerical_moves]
    for i in range(robots - 1):
        # print(i, len(possibilities))
        possibilities = [next_p for p in possibilities for next_p in input_for_output(*p)]
        # now for some pruning; assume that any non-shortest intermediate sequence is not worth pursuing further
        min_size = min(sum(moves.values()) for _, moves in possibilities)
        possibilities = [(start, moves) for start, moves in possibilities if sum(moves.values()) == min_size]
    return min(sum(moves.values()) + 1 for _, moves in possibilities)

def complexity(output, robots):
    min_input = find_best(output, robots)
    print(output, min_input) # i'm leaving this in because otherwise part 2 just takes a couple minutes with no feedback
    numeric_part = int(output[:-1])
    return min_input * numeric_part

print(sum(complexity(output, 3) for output in lines))

# this works but takes QUITE A WHILE and sometimes crashes for no reason
# i think something in my computer is slightly corrupt because other big data puzzles sometimes crash too
# but there must be a better way to prune this
print(sum(complexity(output, 26) for output in lines))

