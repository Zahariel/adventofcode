
with open("input.txt") as f:
    adaptors = [int(line.strip()) for line in f]

adaptors.sort()

adaptors.append(adaptors[-1] + 3)

MAX_JUMP = 3

current = 0
steps = [0] * MAX_JUMP
for rating in adaptors:
    steps[rating - current - 1] += 1
    current = rating

print(steps, steps[0] * steps[2])

current = 0
prev = [0, 0, 1]
for rating in adaptors:
    ways = sum(prev[rating-current-1:])
    prev = prev[rating-current:] + ([0]*(rating-current-1)) + [ways]
    current = rating

print(prev)
