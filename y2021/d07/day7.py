import statistics

def parse(line):
    return line.strip()

with open("input.txt") as f:
    line = f.readline()
    data = [int(n) for n in line.strip().split(",")]

# part 1
target = int(statistics.median(data))
print(target)
print(sum(abs(n - target) for n in data))

# part 2
target = int(statistics.mean(data))
print(target)
print(sum((abs(n - target) * (abs(n - target) + 1)) // 2 for n in data))
print(sum((abs(n - target - 1) * (abs(n - target - 1) + 1)) // 2 for n in data))
