from parsy import char_from, regex, seq, string, whitespace

from parsing import number

DIRS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

def parse(line):
    parser = seq(
        char_from("UDLR").map(lambda c: DIRS[c]) << whitespace,
        number << whitespace,
        string("(#") >> regex(r"[1234567890abcdef]{6}") << string(")")
    ).map(tuple)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]


def get_area(lines):
    r, c = (0, 0)
    twice_area = 0
    perimeter = 0

    for ((dr, dc), dist, _) in lines:
        r2, c2 = r + dist * dr, c + dist * dc
        twice_area += (r * c2 - c * r2)
        perimeter += dist
        r, c = r2, c2

    return int(abs(twice_area) / 2 + perimeter / 2 + 1)

print(get_area(lines))



HEX_DIRS = [DIRS["RDLU"[d]] for d in range(4)]

new_lines = [(HEX_DIRS[int(code[5])], int(code[:5], 16), None) for (_, _, code) in lines]
print(get_area(new_lines))
