import operator
from functools import reduce

from parsy import regex, whitespace

from parsing import number

def parse(line):
    parser = regex(r"\w+:") >> whitespace >> number.sep_by(whitespace)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]


races = list(zip(lines[0], lines[1]))

def beatable(time, record):
    return sum(1 for hold in range(time) if hold * (time - hold) > record)

print(reduce(operator.mul, (beatable(*race) for race in races)))

# part 2

time = int("".join(str(time) for time, _ in races))
record = int("".join(str(record) for _, record in races))

print(beatable(time, record))
