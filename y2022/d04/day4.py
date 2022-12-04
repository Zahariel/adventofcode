import re

def parse(line):
    start1, end1, start2, end2 = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line).groups()
    return int(start1), int(end1), int(start2), int(end2)

with open("input.txt") as file:
    lines = [parse(line.strip()) for line in file]

print(lines)

def fully_contains(start1, end1, start2, end2):
    if start1 <= start2 and end1 >= end2: return True
    if start2 <= start1 and end2 >= end1: return True
    return False

print(sum(1 for pair in lines if fully_contains(*pair)))

def overlaps(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

print(sum(1 for pair in lines if overlaps(*pair)))
