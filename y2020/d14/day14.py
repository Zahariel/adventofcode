import re
from collections import defaultdict

BITSIZE = 36

class Mask:
    def __init__(self, bits):
        self.and_ = (1<<BITSIZE - 1) - sum(2**i for i, bit in enumerate(reversed(bits)) if bit == '0')
        self.or_ = sum(1<<i for i, bit in enumerate(reversed(bits)) if bit == '1')
        self.xs = [i for i, bit in enumerate(reversed(bits)) if bit == 'X']

    def apply_v1(self, val):
        return (val & self.and_) | self.or_

    def locs_v2(self, loc):
        loc |= self.or_
        yield from locs_inner(loc, self.xs, 0)

def locs_inner(loc, xs, idx):
    if idx == len(xs):
        yield loc
    else:
        yield from locs_inner(loc & ~(1<<xs[idx]), xs, idx+1)
        yield from locs_inner(loc | (1<<xs[idx]), xs, idx+1)

class Mem:
    def __init__(self, loc, val):
        self.loc = int(loc)
        self.val = int(val)

def parse(line):
    mask_match = re.fullmatch(rf"mask = ([01X]{{{BITSIZE}}})", line)
    if mask_match:
        return Mask(mask_match[1])
    mem_match = re.fullmatch(r"mem\[(\d+)\] = (\d+)", line)
    if mem_match:
        return Mem(mem_match[1], mem_match[2])
    raise ValueError(f"couldn't parse {line}")

with open("input.txt") as f:
    commands = [parse(line.strip()) for line in f]


current_mask = Mask("X" * BITSIZE)
# using defaultdict as a sparse array here
mem = defaultdict(lambda: 0)
for command in commands:
    if isinstance(command, Mask):
        current_mask = command
    elif isinstance(command, Mem):
        mem[command.loc] = current_mask.apply_v1(command.val)

print(sum(mem.values()))

# part 2
current_mask = Mask("0" * BITSIZE)
mem = defaultdict(lambda: 0)
for command in commands:
    if isinstance(command, Mask):
        current_mask = command
    elif isinstance(command, Mem):
        for loc in current_mask.locs_v2(command.loc):
            mem[loc] = command.val

print(sum(mem.values()))
