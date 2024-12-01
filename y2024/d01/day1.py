from collections import Counter

from parsy import seq, whitespace

from parsing import number


def parse(line):
    return seq(number << whitespace, number).parse(line)

with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

left = [num for (num, _) in lines]
right = [num for (_, num) in lines]

sorted_left = list(sorted(left))
sorted_right = list(sorted(right))

print(sum(abs(l - r) for (l, r) in zip(sorted_left, sorted_right)))

right_counter = Counter(right)
print(sum(l * right_counter[l] for l in left))
