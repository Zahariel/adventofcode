
class IntComp():
    def __init__(self, cells, input_fn=input, output_fn=print):
        self.cells = cells
        self.input_fn = input_fn
        self.output_fn = output_fn
        self.ip = 0

        def get_operand(mode, val):
            if mode == '0':
                return self.cells[val]
            elif mode == '1':
                return val

        def get_operands(count):
            opcode = self.cells[self.ip]
            modes = str(opcode).zfill(count+2)[:-2]
            return tuple(get_operand(modes[-i-1], self.cells[self.ip + 1 + i]) for i in range(count))

        def make_arith_op(argc, fn):
            def op():
                argv = get_operands(argc)
                self.cells[self.cells[self.ip+argc+1]] = fn(*argv)
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

        self.ops = [
            None,
            add_op,
            mult_op,
            input_op,
            output_op,
            jump_if_true,
            jump_if_false,
            less_than_op,
            equal_to_op
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
