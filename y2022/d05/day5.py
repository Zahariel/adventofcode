import re
from collections import defaultdict

import parsing

def parse(line):
    amount, start, end = re.match(r"move (\d+) from (\d+) to (\d+)", line).groups()
    return int(amount), int(start), int(end)

with open("input.txt") as file:
    [top, bottom] = parsing.split_on_blank(file)

    instructions = [parse(line.rstrip()) for line in bottom]

    stacks = defaultdict(list)
    for line in top[:-1]:
        boxes = parsing.chunks(line.rstrip(), 4)
        for i, box in enumerate(boxes):
            if len(box) < 3: continue
            if box[1] == ' ': continue
            stacks[i].insert(0, box[1])

print(stacks)
stacks = [stacks[i] for i in sorted(stacks.keys())]
print(stacks)

# part 1, remember to clone initial
working = [stack[:] for stack in stacks]

def run_instruction(amount, start, end):
    for _ in range(amount):
        if len(working[start - 1]) == 0:
            print()
        working[end - 1].append(working[start - 1].pop())

for inst in instructions:
    run_instruction(*inst)

print("".join(stack[-1] for stack in working))

# part 2
working = [stack[:] for stack in stacks]
def run_inst2(amount, start, end):
    working[end-1].extend(working[start-1][-amount:])
    working[start-1][-amount:] = []

for inst in instructions:
    run_inst2(*inst)

print("".join(stack[-1] for stack in working))

