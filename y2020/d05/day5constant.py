import functools

def parse(line):
    return [c == 'B' or c == 'R' for c in line]

def seat_id(ticket):
    return sum(2**i for i, val in enumerate(reversed(ticket)) if val)

def accumulate(acc, id):
    mn, mx, val = acc
    mn = min(mn, id)
    mx = max(mx, id)
    val ^= id
    return mn, mx, val

with open("input.txt") as f:
    input = (seat_id(parse(line.strip())) for line in f)
    result = (lowest, highest, _) = functools.reduce(accumulate, input, (0, 0x3FF, 0))
    print(highest)

    # fun fact: (4n) ^ (4n+1) ^ (4n+2) ^ (4n+3) == 0 always
    # so extend lowest and highest to be 4n and 4m+3 respectively
    result = functools.reduce(accumulate, range(lowest & 0x3FC, lowest), result)
    _, _, acc = result = functools.reduce(accumulate, range(highest+1, highest | 3), result)
    print(acc)
