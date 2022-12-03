import operator
from functools import reduce

from parsing import chunks

def parse(line):
    split = len(line)//2
    return line[:split],line[split:]

with open("input.txt") as lines:
    sacks = [parse(line.strip()) for line in lines]

print(sacks)

def priority(item):
    if 'a' <= item <= 'z':
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27

def find_error(sack):
    left, right = sack
    left = set(left)
    right = set(right)
    error = left & right
    return error.pop()

print([find_error(sack) for sack in sacks])
print(sum(priority(find_error(sack)) for sack in sacks))

def find_badge(sacks):
    return reduce(operator.and_, (set(left) | set(right) for (left, right) in sacks)).pop()

print([find_badge(group) for group in chunks(sacks, 3)])
print(sum(priority(find_badge(group)) for group in chunks(sacks, 3)))
