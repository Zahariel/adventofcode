import math

from parsy import regex, seq, string

from parsing import split_on_blank

def parse(line):
    node = regex(r"...")
    parser = seq(node << string(" = ("),
                 node << string(", "),
                 node << string(")")).map(tuple)
    return parser.parse(line)

with open("input.txt") as file:
    groups = list(split_on_blank(file))
    instructions = groups[0][0]

    nodes = [parse(line.rstrip()) for line in groups[1]]

node_map = {node: {"L": left, "R": right} for (node, left, right) in nodes}

def find_time(start, target_fn):
    current = start
    steps = 0
    while not target_fn(current):
        current = node_map[current][instructions[steps % len(instructions)]]
        steps += 1
    return steps

print(find_time("AAA", lambda n: n == "ZZZ"))

# part 2

starts = [node for node in node_map if node[-1] == 'A']

times = [find_time(start, lambda n: n[-1] == 'Z') for start in starts]
print(math.lcm(*times))
