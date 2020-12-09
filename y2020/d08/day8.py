import re

from y2020.computer import Computer

def parse(line):
    inst, val = re.fullmatch(r"(.+) ([-+]\d+)", line).groups()
    return inst, int(val)

with open("input.txt") as f:
    instructions = [parse(line.strip()) for line in f]

computer = Computer(instructions)
print(computer.run_until_loop())

for i, (inst, val) in enumerate(instructions):
    if inst == "acc": continue
    elif inst == "nop": new_inst = "jmp"
    elif inst == "jmp": new_inst = "nop"
    else: raise NotImplementedError(f"unexpected instruction {inst}")

    instructions[i] = (new_inst, val)
    computer.reset()
    complete, result = computer.run_until_loop()
    if complete:
        print(result)
        break
    instructions[i] = (inst, val)

