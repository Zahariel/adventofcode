def parse(line):
    return [int(c) for c in line]

with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

# part 1 solution obviated by generic solution to part 2
# def joltage(line):
#     tens, tensidx = max((batt, -i) for i, batt in enumerate(line[:-1]))
#     tensidx = -tensidx
#     ones = max(batt for batt in line[tensidx+1:])
#     return 10 * tens + ones
#
# print(sum(joltage(line) for line in lines))

def joltage_n(line, places):
    value = 0
    idx = 0
    for place in range(places-1, -1, -1):
        digit, neg_new_idx = max((batt, -(idx+i)) for i, batt in enumerate(line[idx:len(line)-place]))
        value = value * 10 + digit
        idx = -neg_new_idx + 1
    return value

print(sum(joltage_n(line, 2) for line in lines))
print(sum(joltage_n(line, 12) for line in lines))
