import re


def parse(line):
    return [(int(l), int(r)) for (l, r) in re.findall(r"mul\((\d+),(\d+)\)", line)]


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

print(sum(l * r for line in lines for (l, r) in line))


def parse2(line):
    return re.findall(r"(mul)\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)", line)

with open("input.txt") as f:
    lines = [parse2(line.rstrip()) for line in f]

total = 0
active = True
for line in lines:
    for mul, l, r, do, dont in line:
        if active and mul == "mul":
            total += int(l) * int(r)
        elif do == "do":
            active = True
        elif dont == "don't":
            active = False

print(total)
