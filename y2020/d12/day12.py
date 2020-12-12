import re

def parse(line):
    dir, amt = re.fullmatch(r"(.)(\d+)", line).groups()
    return dir, int(amt)

with open("input.txt") as f:
    instructions = [parse(line.strip()) for line in f]

MOVES = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}
x, y = 0, 0
dx, dy = MOVES['E']

for dir, amt in instructions:
    if dir in MOVES:
        movex, movey = MOVES[dir]
    elif dir == 'F':
        movex, movey = dx, dy
    else:
        movex, movey = 0, 0
        if dir == 'L':
            while amt > 0:
                dx, dy = dy, -dx
                amt -= 90
        elif dir == 'R':
            while amt > 0:
                dx, dy = -dy, dx
                amt -= 90
    x, y = x + amt * movex, y + amt * movey

print(x, y, abs(x) + abs(y))


# part 2
x, y = 0, 0
wx, wy = 10, -1

for dir, amt in instructions:
    if dir in MOVES:
        movex, movey = MOVES[dir]
        wx, wy = wx + movex * amt, wy + movey * amt
    elif dir == 'F':
        x, y = x + wx * amt, y + wy * amt
    elif dir == 'L':
        while amt > 0:
            wx, wy = wy, -wx
            amt -= 90
    elif dir == 'R':
        while amt > 0:
            wx, wy = -wy, wx
            amt -= 90

print(x, y, abs(x) + abs(y))
