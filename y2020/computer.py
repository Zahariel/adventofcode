
microcode = {
    "nop": lambda val, pc, acc: (pc + 1, acc),
    "jmp": lambda val, pc, acc: (pc + val, acc),
    "acc": lambda val, pc, acc: (pc + 1, acc + val),
}

class Computer():
    def __init__(self, instructions):
        self.instructions = instructions
        self.acc = 0
        self.pc = 0

    def reset(self):
        self.acc = 0
        self.pc = 0

    def run_until_loop(self):
        seen = set()
        while True:
            if self.pc in seen:
                return False, self.acc
            seen.add(self.pc)
            if self.pc >= len(self.instructions):
                return True, self.acc
            self.one_step()


    def one_step(self):
        inst, val = self.instructions[self.pc]
        if inst in microcode:
            self.pc, self.acc = microcode[inst](val, self.pc, self.acc)
        else:
            raise NotImplementedError(f"unexpected instruction {inst}")
