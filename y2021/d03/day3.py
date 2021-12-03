
def parse(line):
    return line.strip()

with open("input.txt") as f:
    lines = f.readlines()
    input = [parse(line) for line in lines]

def analyze(numbers):
    zeroes = [0 for _ in numbers[0]]
    ones = [0 for _ in numbers[0]]
    for l in numbers:
        for i, c in enumerate(l):
            if c == '0':
                zeroes[i] += 1
            else:
                ones[i] += 1
    return zeroes, ones

zeroes, ones = analyze(input)

gamma = 0
epsilon = 0
for i in range(len(zeroes)):
    gamma *= 2
    epsilon *= 2
    if zeroes[i] > ones[i]:
        gamma += 1
    else:
        epsilon += 1

print(gamma, epsilon, gamma * epsilon)

# part 2

def filter_to(ch, idx, l):
    return list(filter(lambda n: n[idx] == ch, l))

oxy = list(input)
co2 = list(input)

for i in range(len(input[0])):
    zeroes, ones = analyze(oxy)
    if zeroes[i] > ones[i]:
        oxy = filter_to('0', i, oxy)
    else:
        oxy = filter_to('1', i, oxy)

    if len(co2) == 1: continue
    zeroes, ones = analyze(co2)
    if zeroes[i] > ones[i]:
        co2 = filter_to('1', i, co2)
    else:
        co2 = filter_to('0', i, co2)

print(oxy, co2)

print(int(oxy[0], 2) * int(co2[0], 2))