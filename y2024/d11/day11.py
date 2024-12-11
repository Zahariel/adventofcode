from collections import Counter

from parsy import whitespace

from parsing import number


def parse(line):
    return number.sep_by(whitespace).parse(line)

with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

stones = Counter(lines[0])

def process(stones):
    result = Counter()
    for num, count in stones.items():
        if num == 0:
            result[1] += count
            continue
        num_str = str(num)
        if len(num_str) % 2 == 0:
            left, right = num_str[:len(num_str)//2], num_str[len(num_str)//2:]
            result[int(left)] += count
            result[int(right)] += count
        else:
            result[num * 2024] = count
    return result

BLINKS = 25
for i in range(BLINKS):
    stones = process(stones)

print(sum(stones.values()))

MORE_BLINKS = 75
for i in range(BLINKS, MORE_BLINKS):
    stones = process(stones)

print(sum(stones.values()))
