import operator
from functools import reduce

from parsy import whitespace

from parsing import number, split_on_blank


def parse(line):
    return number.sep_by(whitespace).parse(line)


with open("input.txt") as f:
    lines = [line.rstrip("\n") for line in f.readlines()]

    inputs = [parse(line.rstrip()) for line in lines[:-1]]
    ops = lines[-1].split()

eqns = list(zip(list(zip(*inputs)), ops))

OPS = {
    "+": operator.add,
    "*": operator.mul,
}

def eval_eqn(inputs, op):
    return reduce(OPS[op], inputs)

print(sum(eval_eqn(*eqn) for eqn in eqns))

def parse_eqn2(eqn):
    op = eqn[0][-1]
    eqn[0] = eqn[0][:-1]
    inputs = [int(inp.strip()) for inp in eqn]
    return inputs, op

# fortunately + and * are both commutative so it doesn't matter that the problem specifies right-to-left
# but if that mattered i would actually want to rotate this, not transpose it
# but rotate is equivalent to transpose + reverse order anyway
transposed_lines = list("".join(digits) for digits in zip(*lines))
raw_eqns:list[list[str]] = list(split_on_blank(transposed_lines))
eqns = [parse_eqn2(eqn) for eqn in raw_eqns if len(eqn) > 0]

print(sum(eval_eqn(*eqn) for eqn in eqns))
