from parsy import seq, string

from parsing import number


def parse(line):
    return seq(string("L") | string("R"), number).map(tuple).parse(line)

with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]


dial = 50
password = 0
for dir, dist in lines:
    if dir == "L": dist = -dist
    dial += dist
    dial %= 100
    if dial == 0:
        password += 1

print(password)


dial = 50
password = 0
for dir, dist in lines:
    rots, dist = divmod(dist, 100)
    password += rots
    if dir == "L":
        if dial == 0:
            # fixup for starting at 0
            password -= 1
        dial -= dist
        if dial <= 0:
            password += 1
            dial %= 100
    else:
        dial += dist
        rots, dial = divmod(dial, 100)
        password += rots

print(password)

# bonus kind of silly portion-based solution, loosely based on Alex's
# using portion is tantamount to obliterating this problem with a plasma cannon, but it works
import portion as P
dial = 50
password = 0
for dir, dist in lines:
    rots, dist = divmod(dist, 100)
    password += rots
    if dir == "L":
        clicks = P.closedopen(dial-dist, dial)
        dial -= dist
    else:
        clicks = P.openclosed(dial, dial+dist)
        dial += dist
    dial %= 100
    if 0 in clicks or 100 in clicks:
        password += 1

print(password)
