
class IntComp():
    def __init__(self, cells, input_fn=input, output_fn=print):
        self.cells = list(cells)
        self.input_fn = input_fn
        self.output_fn = output_fn
        self.ip = 0
        self.relative_base = 0

        def ensure_cell(idx):
            if(idx < 0):
                print("invalid index accessed", idx)
                exit(1)
            while(len(self.cells) < idx + 1):
                self.cells.append(0)

        def get_target(mode, val):
            if mode == '0':
                return val
            elif mode == '2':
                return self.relative_base + val
            else:
                print("unexpected address mode", mode)
                exit(2)

        def get_operand(mode, val):
            if mode == '1':
                return val
            else:
                target = get_target(mode, val)
                ensure_cell(target)
                return self.cells[target]

        def get_operands(count, output=False):
            opcode = self.cells[self.ip]
            modes = str(opcode).zfill(count+3)[:-2]
            results = tuple(get_operand(modes[-i - 1], self.cells[self.ip + 1 + i]) for i in range(count))
            if output:
                return results, get_target(modes[0], self.cells[self.ip + 1 + count])
            else:
                return results

        def make_arith_op(argc, fn):
            def op():
                argv, target = get_operands(argc, output=True)
                ensure_cell(target)
                self.cells[target] = fn(*argv)
                return self.ip + argc + 2
            return op

        add_op = make_arith_op(2, lambda a, b: a + b)
        mult_op = make_arith_op(2, lambda a, b: a * b)
        input_op = make_arith_op(0, lambda: int(input_fn("input op:")))
        less_than_op = make_arith_op(2, lambda a, b: 1 if a < b else 0)
        equal_to_op = make_arith_op(2, lambda a, b: 1 if a == b else 0)

        def output_op():
            result, = get_operands(1)
            output_fn(result)
            return self.ip + 2

        def jump_if_true():
            val, target = get_operands(2)
            if val != 0:
                return target
            return self.ip + 3

        def jump_if_false():
            val, target = get_operands(2)
            if val == 0:
                return target
            return self.ip + 3

        def set_relative_base_op():
            amt, = get_operands(1)
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

class InputFunction():
    def __init__(self, list):
        self.list = list
        self.idx = 0

    def __call__(self, *args, **kwargs):
        self.idx = self.idx + 1
        return self.list[self.idx - 1]

class FrameOutput():
    def __init__(self, size, fn):
        self.size = size
        self.fn = fn
        self.outputs = []

    def __call__(self, val):
        self.outputs.append(val)
        if len(self.outputs) == self.size:
            self.fn(*self.outputs)
            self.outputs = []
