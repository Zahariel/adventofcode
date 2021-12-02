
def parse(line):
    dir, dist = line.split(" ")
    return dir, int(dist)


with open("input.txt") as f:
    lines = f.readlines()

    input = [parse(line) for line in lines]

print(input)

horiz = 0
depth = 0

for dir, dist in input:
    if dir == 'forward':
        horiz += dist
    elif dir == 'down':
        depth += dist
    elif dir == 'up':
        depth -= dist

print(horiz, depth, horiz * depth)

horiz = 0
depth = 0
aim = 0
for dir, dist in input:
    if dir == 'forward':
        horiz += dist
        depth += dist * aim
    elif dir == 'down':
        aim += dist
    elif dir == 'up':
        aim -= dist

print(horiz, depth, horiz*depth)
