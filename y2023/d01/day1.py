def parse(line):
    return line.rstrip()

with open("input.txt") as file:
    lines = [parse(line) for line in file]

print(sum(10*digits[0] + digits[-1] for digits in ([int(c) for c in line if c.isdigit()] for line in lines)))


# part 2

digits = ["zzzzzzzzzz", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def hasdigit(line, index):
    if line[index].isdigit():
        return int(line[index])
    for d, w in enumerate(digits):
        if line[i:i+len(w)] == w:
            return d
    return None

calib = 0
for line in lines:
    first = None
    for i in range(len(line)):
        first = hasdigit(line, i)
        if first is not None: break

    last = None
    for i in range(len(line)-1, -1, -1):
        last = hasdigit(line, i)
        if last is not None: break

    calib += 10 * first + last

print(calib)
