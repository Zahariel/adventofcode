from parsing import split_on_blank


def parse(line):
    return line


with (open("input.txt") as f):
    schematics = list(split_on_blank(f, parse))

locks = []
keys = []

for schematic in schematics:
    pins = [sum(1 for line in schematic if line[p] == "#") for p in range(len(schematic[0]))]
    if schematic[0][0] == "#":
        locks.append(tuple(pins))
    else:
        keys.append(tuple(pins))

print(sum(1 for lock in locks for key in keys if all(lp + kp <= 7 for lp, kp in zip(lock, key))))
