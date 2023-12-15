from functools import reduce

from parsy import regex, seq

from parsing import number

def parse(line):
    return line.split(",")

with open("input.txt") as file:
    instructions = parse(file.readline().rstrip())

def goofy_hash(inst):
    return reduce(lambda h, c: (h + ord(c)) * 17 % 256, inst, 0)

print(sum(goofy_hash(inst) for inst in instructions))


def parse_inst(inst):
    return seq(regex(r"\w+"), regex(r"\=|\-"), number.optional()).map(tuple).parse(inst)

instructions = [parse_inst(inst) for inst in instructions]

boxes = [dict() for _ in range(256)]

for label, op, num in instructions:
    box = boxes[goofy_hash(label)]
    if op == '-':
        if label in box:
            del box[label]
    elif op == '=':
        box[label] = num

print(sum((b+1) * (i+1) * num for b, box in enumerate(boxes) for i, (_, num) in enumerate(box.items())))
