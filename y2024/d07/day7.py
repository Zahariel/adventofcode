from parsy import seq, string, whitespace

from parsing import number


def parse(line):
    return seq(number << string(":") << whitespace, number.sep_by(whitespace)).map(tuple).parse(line)


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

ops = [
    lambda l,r: l*r,
    lambda l,r: l+r,
]

def test_helper(objective, operands, acc, operations):
    if not operands:
        return objective == acc
    if acc > objective:
        return False
    first, *rest = operands
    return any(test_helper(objective, rest, op(acc, first), operations) for op in operations)

def test(objective, operands):
    first, *rest = operands
    return test_helper(objective, rest, first, ops)

print(sum(objective for objective, operands in lines if test(objective, operands)))

ops = [lambda l,r: int(str(l) + str(r))] + ops

print(sum(objective for objective, operands in lines if test(objective, operands)))
