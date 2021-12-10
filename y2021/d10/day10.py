import statistics

def parse(line):
    return line.strip()

with open("input.txt") as f:
    lines = f.readlines()
    data = [parse(line) for line in lines]

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

matches = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

# part 1
total = 0
incomplete = []
for line in data:
    stack = []
    for c in line:
        if c in matches:
            if len(stack) > 0 and stack[-1] == matches[c]:
                stack.pop()
            else:
                total += scores[c]
                break
        else:
            stack.append(c)
    else:
        incomplete.append((line, stack))
print(total)

# part 2
scores2 = {
    "(": "1",
    "[": "2",
    "{": "3",
    "<": "4"
}

# is int(_, 5) cheating? yes. do i care? no.
auto_scores = [int("".join(scores2[c] for c in reversed(stack)), 5) for _, stack in incomplete]

print(statistics.median(auto_scores))
