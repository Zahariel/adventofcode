import itertools

def ensure_cell(cells, idx):
    if idx < 0:
        print("invalid index accessed", idx)
        exit(1)
    while len(cells) < idx + 1:
        cells.append(0)

def get_operand(cells, mode, val, relative_base):
    if mode == '1':
        return val
    else:
        target = get_target(mode, val, relative_base)
        ensure_cell(cells, target)
        return cells[target]

def get_target(mode, val, relative_base):
    if mode == '0':
        return val
    elif mode == '2':
        return relative_base + val
    else:
        print("unexpected address mode", mode)
        exit(2)

def get_operands(cells, ip, count, relative_base, output=False):
    opcode = cells[ip]
    modes = str(opcode).zfill(count+3)[:-2]
    results = tuple(get_operand(cells, modes[-i - 1], cells[ip + 1 + i], relative_base) for i in range(count))
    if output:
        return results, get_target(modes[0], cells[ip + 1 + count], relative_base)
    else:
        return results, None


class IntComp:
    def __init__(self, cells, input_fn=input, output_fn=print):
        self.cells = list(cells)
        self.input_fn = input_fn
        self.output_fn = output_fn
        self.ip = 0
        self.relative_base = 0

        def make_arith_op(argc, fn):
            def op():
                argv, target = get_operands(self.cells, self.ip, argc, self.relative_base, output=True)
                ensure_cell(self.cells, target)
                self.cells[target] = fn(*argv)
                return self.ip + argc + 2
            return op

        add_op = make_arith_op(2, lambda a, b: a + b)
        mult_op = make_arith_op(2, lambda a, b: a * b)
        input_op = make_arith_op(0, lambda: int(input_fn("input op:")))
        less_than_op = make_arith_op(2, lambda a, b: 1 if a < b else 0)
        equal_to_op = make_arith_op(2, lambda a, b: 1 if a == b else 0)

        def output_op():
            (result,), _ = get_operands(self.cells, self.ip, 1, self.relative_base)
            output_fn(result)
            return self.ip + 2

        def jump_if_true():
            (val, target), _ = get_operands(self.cells, self.ip, 2, self.relative_base)
            if val != 0:
                return target
            return self.ip + 3

        def jump_if_false():
            (val, target), _ = get_operands(self.cells, self.ip, 2, self.relative_base)
            if val == 0:
                return target
            return self.ip + 3

        def set_relative_base_op():
            (amt,), _ = get_operands(self.cells, self.ip, 1, self.relative_base)
            self.relative_base = self.relative_base + amt
            return self.ip + 2


        self.ops = [
            None,
            add_op,
            mult_op,
            input_op,
            output_op,
            jump_if_true,
            jump_if_false,
            less_than_op,
            equal_to_op,
            set_relative_base_op
        ]

    def run(self):
        self.ip = 0
        while self.cells[self.ip] != 99:
            op = self.cells[self.ip] % 100
            self.ip = self.ops[op]()

    def __call__(self):
        self.run()

def run_comp(cells, input_fn=input, output_fn=print):
    IntComp(cells, input_fn, output_fn).run()

class InputFunction:
    def __init__(self, list):
        self.list = list
        self.idx = 0

    def __call__(self, *args, **kwargs):
        self.idx = self.idx + 1
        return self.list[self.idx - 1]

class FrameOutput:
    def __init__(self, size, fn):
        self.size = size
        self.fn = fn
        self.outputs = []

    def __call__(self, val):
        self.outputs.append(val)
        if len(self.outputs) == self.size:
            self.fn(*self.outputs)
            self.outputs = []

class CoIntComp:
    def __init__(self, cells):
        self.cells = list(cells)
        self.ip = 0
        self.relative_base = 0
        self.inputs = []

        def set_relative_base_op(val):
            self.relative_base = self.relative_base + val
            return self.ip + 2, None

        self.ops = [
            None,
            (lambda a, b: (self.ip + 4, a+b), 2, True),
            (lambda a, b: (self.ip + 4, a*b), 2, True),
            (lambda: (self.ip + 2, self.inputs.pop(0)), 0, True),
            (None, 1, False), # output is handled special
            (lambda val, t: (t if val != 0 else self.ip + 3, None), 2, False),
            (lambda val, t: (t if val == 0 else self.ip + 3, None), 2, False),
            (lambda a, b: (self.ip + 4, 1 if a < b else 0), 2, True),
            (lambda a, b: (self.ip + 4, 1 if a == b else 0), 2, True),
            (set_relative_base_op, 1, False)
        ]

    def decode(self, instruction):
        opcode = instruction % 100
        return self.ops[opcode]

    def run(self, *inputs):
        self.inputs = self.inputs + list(inputs)
        while self.cells[self.ip] != 99:
            instruction = self.cells[self.ip]
            fn, argc, has_output = self.decode(instruction)
            argv, output_target = get_operands(self.cells, self.ip, argc, self.relative_base, has_output)
            if fn is None:
                self.ip = self.ip + 2
                return argv[0]
            else:
                self.ip, result = fn(*argv)
                if has_output:
                    ensure_cell(self.cells, output_target)
                    self.cells[output_target] = result

class AsciiComp(IntComp):
    def __init__(self, cells, instructions):
        inputs = list(itertools.chain(*[[ord(c) for c in line] + [10] for line in instructions]))
        super().__init__(cells, output_fn=lambda c: print(chr(c), end="") if c < 255 else print(c), input_fn=InputFunction(inputs))