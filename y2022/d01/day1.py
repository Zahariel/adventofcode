with open("input.txt") as file:
    elves = []
    elf = []
    for line in file:
        line = line.strip()
        if len(line) == 0:
            elves.append(elf)
            elf = []
        else:
            elf.append(int(line))

    elves.append(elf)

print(elves)

# part 1
print(max(sum(elf) for elf in elves))

# part 2
elves.sort(key=sum, reverse=True)

print(sum(elves[0]) + sum(elves[1]) + sum(elves[2]))
