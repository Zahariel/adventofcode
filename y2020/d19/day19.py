import re

class Rule:
    def __init__(self, tokens):
        self.possibilities = []
        poss = []
        for t in tokens:
            if t == '|':
                self.possibilities.append(poss)
                poss = []
            else:
                poss.append(int(t))
        self.possibilities.append(poss)
        self.regex = None

    def calc_regex(self, rules):
        if not self.regex:
            self.regex = "(?:" + "|".join("(?:" + "".join(rules[i].calc_regex(rules) for i in poss) + ")" for poss in self.possibilities) + ")"
        return self.regex

    def __repr__(self):
        return repr(self.possibilities)

class CharRule:
    def __init__(self, char):
        self.char = char

    def __repr__(self):
        return self.char

    def calc_regex(self, rules):
        return self.char

def parse_rule(line):
    number, body = re.fullmatch(r"(\d+): (.*)", line).groups()
    tokens = body.split()
    if len(tokens) == 1 and tokens[0][0] == '"':
        return int(number), CharRule(tokens[0][1])
    return int(number), Rule(tokens)

with open("input.txt") as f:
    rules = dict()
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        number, rule = parse_rule(line)
        rules[number] = rule

    messages = [line.strip() for line in f]

# there are no loops, so the language is finite. all finite languages are regular
for rule in rules.values():
    rule.calc_regex(rules)

# part 1

pattern_0 = re.compile(rules[0].regex)

print(sum(1 for message in messages if pattern_0.fullmatch(message)))

# part 2: now it's a CFG
# only "0: 8 11", 8, and 11 are modified by the change, fortunately
# 8 is just 42+
# 11 is now 42^n 31^n for n >= 1
# so 8 11 is just 42^n 31^m for n > m >= 1

pattern_42 = re.compile(rules[42].regex)
pattern_31 = re.compile(rules[31].regex)

# this is cheating, A LOT, if 42 and 31 share any common prefixes
# but fortunately (probably not actually luck), they don't
def test_message(message):
    pos = 0
    matches_42 = 0
    while pos < len(message):
        match = pattern_42.match(message, pos)
        if not match:
            break
        matches_42 += 1
        pos = match.end()

    matches_31 = 0
    while pos < len(message):
        match = pattern_31.match(message, pos)
        if not match:
            break
        matches_31 += 1
        pos = match.end()

    return pos == len(message) and matches_42 > matches_31 > 0

print(sum(1 for message in messages if test_message(message)))
