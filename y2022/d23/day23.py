from collections import defaultdict

def parse(line):
    return line

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

ELF = '#'
BLANK = '.'

def print_elves(elves):
    min_x = min(x for (x, y) in elves)
    min_y = min(y for (x, y) in elves)
    max_x = max(x for (x, y) in elves)
    max_y = max(y for (x, y) in elves)

    blanks = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(ELF if (x, y) in elves else BLANK, end="")
            blanks += 0 if (x, y) in elves else 1
        print(" ", y)
    return blanks

# part 1
elves = {(x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == ELF}
print_elves(elves)

directions = [
    ([-1, 0, 1], [-1], 0, -1),
    ([-1, 0, 1], [1], 0, 1),
    ([-1], [-1, 0, 1], -1, 0),
    ([1], [-1, 0, 1], 1, 0),
]

def check(elves, x, y, dxs, dys):
    return all((x + dx, y + dy) not in elves for dx in dxs for dy in dys)

def one_turn(elves, directions):
    targeted = defaultdict(set)

    result = set()
    for x, y in elves:
        neighbors = sum(1 for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (x + dx, y + dy) in elves)
        if neighbors == 1:
            result.add((x, y))
        else:
            for dxs, dys, dx, dy in directions:
                if check(elves, x, y, dxs, dys):
                    targeted[x + dx, y + dy].add((x, y))
                    break
            else:
                result.add((x, y))

    to_delete = set()
    for (x, y), actors in targeted.items():
        if len(actors) > 1:
            for x2, y2 in actors:
                result.add((x2, y2))
            to_delete.add((x, y))

    for x, y in to_delete:
        del targeted[x, y]

    result.update(targeted.keys())

    directions = directions[1:] + [directions[0]]
    return result, directions, result == elves

ROUNDS = 10

for _ in range(ROUNDS):
    elves, directions, _ = one_turn(elves, directions)

answer = print_elves(elves)
print(answer)

# part 2
round = ROUNDS
done = False
while not done:
    elves, directions, done = one_turn(elves, directions)
    round += 1

print(round)
