
sum = 0

with open("input.txt") as f:
    for line in f:
        module = int(line)
        while module > 0:
            module = max(0, module // 3 - 2)
            sum = sum + module

print(sum)