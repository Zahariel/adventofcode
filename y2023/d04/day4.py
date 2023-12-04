from collections import defaultdict

from parsy import seq, string, whitespace

from parsing import number

def parse(line):
    parser = seq(
        string("Card") >> whitespace >> number << string(":") << whitespace,
        number.sep_by(whitespace).map(set) << whitespace << string("|"),
        whitespace >> number.sep_by(whitespace).map(set),
    ).map(tuple)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

print(lines)

print(sum(int(2 ** (len(wins & choices) - 1)) for _, wins, choices in lines))



copies = defaultdict(int)
for n, wins, choices in lines:
    copies[n] += 1
    success = len(wins & choices)
    for i in range(n+1, n+1+success):
        copies[i] += copies[n]

print(sum(copies.values()))
