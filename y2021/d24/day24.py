import re

class Instruction:
    def __init__(self, opcode, first, second):
        self.opcode = opcode
        self.first = first
        self.second = second

    def __repr__(self):
        return f"Instruction({self.opcode}, {self.first}, {self.second})"

def parse(line):
    opcode, left, right = re.match(r"(...) (\S+)(?: (\S+))?", line.rstrip()).groups()
    return Instruction(opcode, left, right)

with open("input.txt") as f:
    data = [parse(line) for line in f.readlines() if line[0] != "#"]

def arg_parse(arg, vars):
    if arg in vars:
        return vars[arg]
    return int(arg)

def run_program(insts):
    vars = {'w':0, 'x':0, 'y':0, 'z':0}
    idx = 0
    for inst in insts:
        if inst.opcode == 'inp':
            print(vars)
            print(idx, vars['z'] % 26)
            val = int(input())
            idx += 1
            vars[inst.first] = val
        elif inst.opcode == 'add':
            vars[inst.first] += arg_parse(inst.second, vars)
        elif inst.opcode == 'mul':
            vars[inst.first] *= arg_parse(inst.second, vars)
        elif inst.opcode == 'div':
            vars[inst.first] //= arg_parse(inst.second, vars)
        elif inst.opcode == 'mod':
            vars[inst.first] %= arg_parse(inst.second, vars)
        elif inst.opcode == 'eql':
            vars[inst.first] = 1 if vars[inst.first] == arg_parse(inst.second, vars) else 0
    print(vars)

run_program(data)


# checked digits: 3, 7, 8, 10, 11, 12, 13

# i[3] == i[2] + 4
# i[7] == i[6] + 3
# i[8] = i[5] + 5
# i[10] = i[9] - 8
# i[11] = i[4] - 2
# i[12] = i[1] - 6
# i[13] = i[0] + 7

# 01234567890123
# 29599469991739

# part 2
# 01234567890123
# 17153114691118
