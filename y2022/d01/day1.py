import parsing

with open("input.txt") as file:
    elves = list(parsing.split_on_blank(file, int))

print(elves)

# part 1
print(max(sum(elf) for elf in elves))

# part 2
elves.sort(key=sum, reverse=True)

print(sum(sum(elf) for elf in elves[:3]))
