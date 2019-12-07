with open("input.txt") as f:
    line1 = f.readline()
    line2 = f.readline()


def calc_pos_set(line):
    x, y, d = 0, 0, 0
    result = {}
    for inst in line.split(","):
        dir = inst[0]
        dist = int(inst[1:])
        if dir == 'U':
            for yy in range(y, y+dist):
                result.setdefault((x, yy), d)
                d = d + 1
            y = y + dist
        elif dir == 'D':
            for yy in range(y, y-dist, -1):
                result.setdefault((x, yy), d)
                d = d + 1
            y = y - dist
        elif dir == 'L':
            for xx in range(x, x-dist, -1):
                result.setdefault((xx, y), d)
                d = d + 1
            x = x - dist
        elif dir == 'R':
            for xx in range(x, x+dist):
                result.setdefault((xx, y), d)
                d = d + 1
            x = x + dist
        else:
            print("unknown direction", dir)
    result.setdefault((x, y), d)
    del result[0,0]
    return result


wire1 = calc_pos_set(line1)
wire2 = calc_pos_set(line2)

crosses = wire1.keys() & wire2.keys()

print(crosses)

print(min(wire1[x, y] + wire2[x, y] for (x, y) in crosses))

