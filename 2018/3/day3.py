import re
fabric = [[0 for i in range(1000)] for j in range(1000)]

pattern = re.compile(r"\#(?P<elf>\d+) \@ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)")
def parse(line):
    match = pattern.match(line).groupdict()
    return (int(match["elf"]), int(match["left"]), int(match["top"]), int(match["width"]), int(match["height"]))

with open("day3input.txt") as file:
    for line in file:
        (elf, left, top, width, height) = parse(line)
        for i in range(top, top+height):
            for j in range(left, left+width):
                fabric[i][j] += 1

print(sum(1 for row in fabric for n in row if n > 1))

def test(left, top, width, height):
    return all(n < 2 for row in fabric[top:top+height] for n in row[left:left+width])

with open("day3input.txt") as file:
    print([elf for (elf, left, top, width, height) in (parse(line) for line in file) if test(left, top, width, height)])
