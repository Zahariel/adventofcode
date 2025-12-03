from parsy import seq, string

from parsing import number


def parse(line):
    rng = seq(number, string("-") >> number).map(tuple)
    return rng.sep_by(string(",")).parse(line)

with open("input.txt") as f:
    ranges = parse(f.readline().rstrip())

# there's probably a better way to do this but I only have about 3M numbers to check,
# it's easy enough to just check them all one by one

def validate_id(id):
    idstr = str(id)
    if len(idstr) % 2 == 1: return True
    left = idstr[:len(idstr)//2]
    right = idstr[len(idstr)//2:]
    if left == right: return False
    return True

print(sum(id for left, right in ranges for id in range(left, right + 1) if not validate_id(id)))

def validate_id2(id):
    idstr = str(id)
    for part_size in range(1, len(idstr)//2 + 1):
        if len(idstr) % part_size != 0: continue
        parts = [idstr[idx:idx+part_size] for idx in range(0, len(idstr), part_size)]
        if all(part == parts[0] for part in parts[1:]): return False
    return True

print(sum(id for left, right in ranges for id in range(left, right+1) if not validate_id2(id)))

# bonus totally cheating solution inspired by david
import re

part_1 = re.compile(r"(\d+)\1")
print(sum(id for left, right in ranges for id in range(left, right+1) if part_1.fullmatch(str(id))))
part_2 = re.compile(r"(\d+)\1+")
print(sum(id for left, right in ranges for id in range(left, right+1) if part_2.fullmatch(str(id))))
