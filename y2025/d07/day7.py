
with open("input.txt") as f:
    lines = [line.rstrip() for line in f]


counts = [[1 if c == 'S' else 0 for c in line] for line in lines]
splits = 0
for y, line in enumerate(counts[:-1]):
    for x, count in enumerate(line):
        if count > 0:
            below = lines[y + 1][x]
            if below == '^':
                splits += 1
                counts[y + 1][x - 1] += count
                counts[y + 1][x + 1] += count
            else:
                counts[y + 1][x] += count

print(splits)
print(sum(counts[-1]))
