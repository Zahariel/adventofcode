with open("day13input.txt") as file:
    grid = [[c for c in line.rstrip()] for line in file]

carts = [[None for x in line] for line in grid]

replacements = {"<": ((-1, 0, 0), "-"), ">": ((1, 0, 0), "-"), "^": ((0, -1, 0), "|"), "v": ((0, 1, 0), "|")}

for (y, line) in enumerate(grid):
    for (x, char) in enumerate(line):
        if char in replacements:
            carts[y][x], grid[y][x] = replacements[char]

def turnLeft(dx, dy): return dy, -dx
def straight(dx, dy): return dx, dy
def turnRight(dx, dy): return -dy, dx
turns = [turnLeft, straight, turnRight]

def doStep(grid, carts):
    newCarts = [[None for x in line] for line in carts]
    count = 0
    for y, line in enumerate(carts):
        for x, cart in enumerate(line):
            if cart is None: continue
            (dx, dy, state) = cart
            xx, yy = x + dx, y + dy
            if (yy, xx) > (y, x) and carts[yy][xx] is not None:
                print(x, y, cart, "vs", xx, yy, carts[yy][xx])
                carts[yy][xx] = None
                continue
            if (yy, xx) < (y, x) and newCarts[yy][xx] is not None:
                print(x, y, cart, "vs", xx, yy, newCarts[yy][xx], "new")
                newCarts[yy][xx] = None
                count -= 1
                continue
            count += 1
            track = grid[yy][xx]
            if track == "|" or track == "-":
                newCarts[yy][xx] = cart
            elif track == "+":
                dx, dy = turns[state](dx, dy)
                newCarts[yy][xx] = (dx, dy, (state + 1) % 3)
            elif track == "/":
                newCarts[yy][xx] = (-dy, -dx, state)
            elif track == "\\":
                newCarts[yy][xx] = (dy, dx, state)
    return count, newCarts

numCarts = sum(1 for line in carts for cart in line if cart is not None)
time = 0
while time < 100000 and numCarts > 1:
    if time % 1000 == 0:
        print(time, numCarts)
    numCarts, carts = doStep(grid, carts)
    time += 1

print([(x, y) for y, line in enumerate(carts) for x, cart in enumerate(line) if cart is not None])