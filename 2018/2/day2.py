from collections import Counter

twos = 0
threes = 0
with open("day2input.txt") as file:
    for line in file:
        alphagram = Counter(line.strip())
        if 2 in alphagram.values():
            twos += 1
        if 3 in alphagram.values():
            threes += 1
    print(twos * threes)

def diffs(left, right):
    count = 0
    for (i,j) in zip(left, right):
        if i != j:
            count += 1
    return count

with open("day2input.txt") as file:
    boxes = [line.strip() for line in file.readlines()]
    close = [(left, right) for left in boxes for right in boxes if diffs(left, right) == 1]
    print(close)
