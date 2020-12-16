import re

class Rule:
    def __init__(self, name, start1, end1, start2, end2):
        self.name = name
        self.start1 = int(start1)
        self.end1 = int(end1)
        self.start2 = int(start2)
        self.end2 = int(end2)

    def is_in(self, num):
        return self.start1 <= num <= self.end1 or self.start2 <= num <= self.end2

    def __str__(self):
        return f"Rule: {self.name}"

    def __repr__(self):
        return f"Rule({self.name})"

def parse_rule(line):
    name, start1, end1, start2, end2 = re.fullmatch(r"(.+): (\d+)-(\d+) or (\d+)-(\d+)", line).groups()
    return Rule(name, start1, end1, start2, end2)

with open("input.txt") as f:
    rules = []
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        rules.append(parse_rule(line))

    # your ticket
    f.readline()

    your_ticket = [int(v) for v in f.readline().strip().split(',')]

    # blank line
    f.readline()

    # "nearby tickets"
    f.readline()

    nearby_tickets = []
    for line in f:
        nearby_tickets.append([int(v) for v in line.strip().split(',')])


# part 1

def value_totally_invalid(num):
    return not any(rule.is_in(num) for rule in rules)

totally_invalid_sum = sum(val for ticket in nearby_tickets for val in ticket if value_totally_invalid(val))
print(totally_invalid_sum)

# part 2
# destroy any totally invalid tickets
nearby_tickets = list(filter(lambda ticket: all(not value_totally_invalid(val) for val in ticket), nearby_tickets))

# each slot of possibilities is the list of rules that slot could still be
possibilities = [set(rules) for pos in nearby_tickets[0]]

for ticket in nearby_tickets:
    for pos, val in enumerate(ticket):
        for rule in rules:
            if rule in possibilities[pos] and not rule.is_in(val):
                possibilities[pos].remove(rule)

decisions = [None for _ in possibilities]
while any(val is None for val in decisions):
    # find something with 1 possibility
    idx, s = next(filter(lambda p: len(p[1]) == 1, enumerate(possibilities)))
    val = s.pop()
    decisions[idx] = val
    # take that possibility out of everything
    [poss.discard(val) for poss in possibilities]

product = 1
for val, rule in zip(your_ticket, decisions):
    if rule.name.startswith("departure"):
        product *= val

print(product)

