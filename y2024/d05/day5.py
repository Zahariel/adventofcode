from collections import defaultdict
from functools import cmp_to_key
from itertools import combinations

from parsy import seq, string

from parsing import number, split_on_blank


def parse_rule(line):
    return seq(number << string("|"), number).map(tuple).parse(line)

def parse_update(update):
    return number.sep_by(string(",")).parse(update)

with open("input.txt") as f:
    rules, updates = split_on_blank(f)

    rules = [parse_rule(rule) for rule in rules]
    updates = [parse_update(update) for update in updates]

rules_dict = defaultdict(set)
for l, r in rules:
    rules_dict[l].add(r)

def check_update(update):
    return not any(p1 in rules_dict[p2] for p1, p2 in combinations(update, 2))

print(sum(update[len(update) // 2] for update in updates if check_update(update)))

def fix_update(update):
    return sorted(update,
                  key=cmp_to_key(lambda l, r: -1 if r in rules_dict[l] else 1 if l in rules_dict[r] else 0))

print(sum(fix_update(update)[len(update) // 2] for update in updates if not check_update(update)))
