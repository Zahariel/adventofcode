import re
from breadth_first import breadth_first
from collections import defaultdict

from keyeddefaultdict import KeyedDefaultdict

def parse(line):
    name, contents_str = re.fullmatch(r"(.+) bags contain (.+)\.", line).groups()
    if contents_str == "no other bags":
        return name, []
    contents = [re.fullmatch(r"(\d+) (.+) bags?", part.strip()).groups() for part in contents_str.split(',')]
    return name, [(int(amount), partname) for amount, partname in contents]


rules = dict()

with open("input.txt") as f:
    for line in f:
        name, contents = parse(line.strip())
        rules[name] = contents

# part 1
inverted_rules = defaultdict(list)

for key, parts in rules.items():
    for amount, part in parts:
        inverted_rules[part].append((1, key))

can_contain = set()
breadth_first('shiny gold', lambda key: inverted_rules[key], lambda _, key: can_contain.add(key))
# -1 because 'shiny gold' itself isn't counted
print(len(can_contain) - 1)


# part 2
# this is kind of a sleazy trick using KeyedDefaultdict as a memoized depth-first-search tree
def assemble(bag):
    total = 1
    for amount, part in rules[bag]:
        total += amount * fullness[part]
    return total

fullness = KeyedDefaultdict(assemble)

# -1 because 'shiny gold' itself isn't counted
print(fullness['shiny gold'] - 1)
