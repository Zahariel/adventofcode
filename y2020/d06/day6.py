import functools
import operator

def parse(line):
    return set(line)

with open("input.txt") as f:
    lines = [parse(line.strip()) for line in f]

groups = []
acc = []
for person in lines:
    if len(person) == 0:
        groups.append(acc)
        acc = []
    else:
        acc.append(person)
groups.append(acc)

print(sum(len(functools.reduce(operator.or_, group)) for group in groups))

print(sum(len(functools.reduce(operator.and_, group)) for group in groups))
