import re

with open("input.txt") as f:
    [xmin, xmax, ymin, ymax] = [int(num) for num in re.match(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)", f.readline().strip()).groups()]

print(xmin, xmax, ymin, ymax)

def step(x, y, vx, vy):
    x += vx
    y += vy
    if vx > 0: vx -= 1
    vy -= 1
    return x, y, vx, vy

def simulation(vx0, vy0):
    x, y, vx, vy = 0, 0, vx0, vy0
    maxy = 0
    while y >= ymin and x <= xmax:
        x, y, vx, vy = step(x, y, vx, vy)
        if y > maxy: maxy = y
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return maxy
    return None

x_best, y_best, h_best = 0, 0, 0
count = 0
for vx0 in range(xmax+1):
    for vy0 in range(ymin-1, -ymin+1):
        height = simulation(vx0, vy0)
        if height is not None:
            count += 1
            if height > h_best:
                x_best, y_best, h_best = vx0, vy0, height

print(x_best, y_best, h_best)
print(count)

