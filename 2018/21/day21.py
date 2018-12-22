import re

def parse_inst(line):
    op, a, b, c = re.match(r"(\S+) (\d+) (\d+) (\d+)", line).groups()
    return op, int(a), int(b), int(c)

def addr(regs, a, b):
    return regs[a] + regs[b]

def addi(regs, a, b):
    return regs[a] + b

def mulr(regs, a, b):
    return regs[a] * regs[b]

def muli(regs, a, b):
    return regs[a] * b

def banr(regs, a, b):
    return regs[a] & regs[b]

def bani(regs, a, b):
    return regs[a] & b

def borr(regs, a, b):
    return regs[a] | regs[b]

def bori(regs, a, b):
    return regs[a] | b

def setr(regs, a, b):
    return regs[a]

def seti(regs, a, b):
    return a

def gtir(regs, a, b):
    return 1 if a > regs[b] else 0

def gtri(regs, a, b):
    return 1 if regs[a] > b else 0

def gtrr(regs, a, b):
    return 1 if regs[a] > regs[b] else 0

def eqir(regs, a, b):
    return 1 if a == regs[b] else 0

def eqri(regs, a, b):
    return 1 if regs[a] == b else 0

def eqrr(regs, a, b):
    return 1 if regs[a] == regs[b] else 0

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
ops_by_name = dict((op.__name__, op) for op in ops)

def run_opcode(opcode, regs, a, b, c):
    regs[c] = ops_by_name[opcode](regs, a, b)
    return regs

with open("day21input.txt") as file:
    ip = int(re.match(r"#ip (\d)", file.readline()).group(1))
    program = [parse_inst(line) for line in file]
    registers = [0 for _ in range(6)]
    #registers[0] = 1
    cycles = 0
    while 0 <= registers[ip] < len(program):
        # if cycles % 100 == 0:
        #     print(cycles, registers)
        op, a, b, c = program[registers[ip]]
        print(registers, (op, a, b, c), end=" ")
        run_opcode(op, registers, a, b, c)
        print(registers, end="")
        input()
        registers[ip] += 1
        cycles += 1

    registers[ip] -= 1
    print(registers)

