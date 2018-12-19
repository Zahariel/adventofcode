import re

def parse_state(line):
    regs = re.search(r"\[(\d+), (\d+), (\d+), (\d+)\]", line).groups()
    return [int(reg) for reg in regs]

def parse_inst(line):
    ops = re.match(r"(\d+) (\d+) (\d+) (\d+)", line).groups()
    return tuple(int(op) for op in ops)

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

opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

possible_interps = [set(opcodes) for i in range(len(opcodes))]

def run_opcode(opcode, regs, a, b, c):
    regs[c] = opcode(regs, a, b)
    return regs

def interpret(start, command, end):
    op, a, b, c = command
    for opcode in opcodes:
        if run_opcode(opcode, start.copy(), a, b, c) != end:
            possible_interps[op].discard(opcode)

with open("day16input.txt") as file:
    interpretations = []
    line = file.readline()
    while len(line.strip()) > 0:
        start = parse_state(line)
        command = parse_inst(file.readline())
        end = parse_state(file.readline())
        interpret(start, command, end)
        file.readline()
        line = file.readline()

    print([[opcode.__name__ for opcode in remaining] for remaining in possible_interps])

    real_interps = [None for i in possible_interps]
    while any(interp is None for interp in real_interps):
        for i, possible in enumerate(possible_interps):
            if len(possible) == 1:
                real_interps[i] = possible.pop()
                for poss2 in possible_interps:
                    poss2.discard(real_interps[i])
    print([opcode.__name__ for opcode in real_interps])

    regs = [0,0,0,0]
    for line in file:
        if len(line.strip()) == 0: continue
        op, a, b, c = parse_inst(line)
        run_opcode(real_interps[op], regs, a, b, c)

    print(regs)