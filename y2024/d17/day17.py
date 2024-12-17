import parsy
from parsy import string

from parsing import number, split_on_blank


def parse_register(line):
    return (string("Register ") >> parsy.regex(r"A|B|C") >> string(": ") >> number).parse(line)

def parse_instructions(line):
    return (string("Program: ") >> number.sep_by(string(","))).parse(line)

with open("input.txt") as f:
    orig_registers, instructions = split_on_blank(f)
    orig_registers = [parse_register(line) for line in orig_registers]

    instructions = parse_instructions(instructions[0])

# registers[3] is instruction pointer
orig_registers.append(0)
registers = orig_registers[:]

def combo(operand):
    if operand < 4: return operand
    return registers[operand-4]

opcodes = [
    (0, lambda x: registers[0] >> combo(x)),
    (1, lambda x: registers[1] ^ x),
    (1, lambda x: combo(x) & 7),
    (3, lambda x: x-2 if registers[0] else registers[3]),
    (1, lambda x: registers[1] ^ registers[2]),
    (-1, lambda x: combo(x) & 7),
    (1, lambda x: registers[0] >> combo(x)),
    (2, lambda x: registers[0] >> combo(x)),
]

def run_program():
    output = []
    while registers[3] < len(instructions):
        target, op = opcodes[instructions[registers[3]]]
        arg = instructions[registers[3] + 1]
        result = op(arg)
        if target < 0:
            output.append(str(result))
        else:
            registers[target] = result
        registers[3] += 2
    return output

print(",".join(run_program()))

# part 2
def find_octits(A, needed):
    for trial in range(8):
        trial_A = A + trial
        C = (trial_A) >> (trial ^ 5)
        if ((trial ^ 5) ^ C) & 7 == needed:
            yield trial

# calculate this from the end of instructions
def solve(ptr, A):
    if ptr == -1:
        return A
    A <<= 3
    x = instructions[ptr]
    for B in find_octits(A, x ^ 6):
        result = solve(ptr-1, A + B)
        if result is not None: return result

answer = solve(len(instructions) - 1, 0)
print(answer)

