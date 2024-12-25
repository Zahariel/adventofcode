from parsing import split_on_blank


with (open("input.txt") as f):
    schematics = list(split_on_blank(f))

locks = []
keys = []

for schematic in schematics:
    pins = [sum(1 for x in pin if x == "#") for pin in zip(*schematic)]
    if schematic[0][0] == "#":
        locks.append(tuple(pins))
    else:
        keys.append(tuple(pins))

print(sum(1 for lock in locks for key in keys if all(lp + kp <= 7 for lp, kp in zip(lock, key))))
