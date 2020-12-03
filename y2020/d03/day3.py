import re

def parse(line):
    return [c == '#' for c in line]

with open("input.txt") as f:
    data = [parse(line.strip()) for line in f]

def slide(dx, dy):
    x = 0
    y = 0
    trees = 0
    while y < len(data):
        if data[y][x]:
            trees += 1
        x += dx
        y += dy
        x %= len(data[0])
    return trees

t1 = slide(1, 1)
t2 = slide(3, 1)
t3 = slide(5, 1)
t4 = slide(7, 1)
t5 = slide(1, 2)

print(t2)
print(t1 * t2 * t3 * t4 * t5)

