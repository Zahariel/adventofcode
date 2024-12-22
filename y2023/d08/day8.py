import math

from parsy import regex, seq, string

from math_utils import chinese_remainder
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

# an actually correct solution to part 2, because the one above is completely wrong, despite getting the right answer
# because of crocked inputs
def find_loop(start, target_fn):
    current = start
    steps = 0
    seen = {(start, 0)}
    goal_time = None
    while True:
        current = node_map[current][instructions[steps % len(instructions)]]
        steps += 1
        if target_fn(current):
            goal_time = steps
        if (current, steps % len(instructions)) in seen:
            break
        else:
            seen.add((current, steps % len(instructions)))

    return goal_time, steps - (steps % len(instructions))

cycles = [find_loop(start, lambda n: n[-1] == 'Z') for start in starts]

answer, modulus = chinese_remainder(cycles)
required_minimum = max(goal for goal, _ in cycles)
print((answer - required_minimum) % modulus + required_minimum)
