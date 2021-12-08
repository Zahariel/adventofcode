import re
import sys

def parse(line):
    digits, outputs = re.match(r"([^|]+) \| ([^|]+)", line.strip()).groups()
    return [frozenset(digit) for digit in digits.split()], [frozenset(output) for output in outputs.split()]

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

# part 1
count = 0
for _, outputs in data:
    for digit in outputs:
        if len(digit) in {2,3,4,7}:
            count += 1

print(count)

# part 2
total = 0
for digits, outputs in data:
    translation = dict()
    rev_trans = [frozenset()] * 10
    # first do the easy ones
    for digit in digits:
        if len(digit) == 2:
            translation[digit] = 1
            rev_trans[1] = digit
        elif len(digit) == 3:
            translation[digit] = 7
            rev_trans[7] = digit
        elif len(digit) == 4:
            translation[digit] = 4
            rev_trans[4] = digit
        elif len(digit) == 7:
            translation[digit] = 8
            rev_trans[8] = digit

    # now figure out the trickier ones
    for digit in digits:
        if len(digit) == 6:
            # has to be 6, 9, or 0, but only 9 contains 4 and 6 doesn't contain 1
            if digit > rev_trans[4]:
                translation[digit] = 9
                rev_trans[9] = digit
            elif digit > rev_trans[1]:
                translation[digit] = 0
                rev_trans[0] = digit
            else:
                translation[digit] = 6
                rev_trans[6] = digit

    for digit in digits:
        if len(digit) == 5:
            # could be 2, 3, or 5
            # only 3 contains 1; only 5 is contained by 6
            if digit > rev_trans[1]:
                translation[digit] = 3
                rev_trans[3] = digit
            elif digit < rev_trans[6]:
                translation[digit] = 5
                rev_trans[5] = digit
            else:
                translation[digit] = 2
                rev_trans[2] = digit

    # ok everything should be translated
    if frozenset() in rev_trans:
        print("couldn't figure this out", digits, rev_trans)
        sys.exit(1)

    # now compute the number
    number = 1000 * translation[outputs[0]] + 100 * translation[outputs[1]] + 10 * translation[outputs[2]] + translation[outputs[3]]
    total += number

print(total)
