
with open("input.txt") as f:
    line = f.readline()

initial_cells = [int(x) for x in line.split(",")]

def get_operand(cells, mode, val):
    if mode == '0':
        return cells[val]
    elif mode == '1':
        return val

def get_operands(cells, ip, count):
    opcode = cells[ip]
    modes = str(opcode).zfill(count+2)[:-2]
    return tuple(get_operand(cells, modes[-i-1], cells[ip + 1 + i]) for i in range(count))

def make_arith_op(argc, fn):
    def op(cells, ip):
        argv = get_operands(cells, ip, argc)
        cells[cells[ip+argc+1]] = fn(*argv)
        return ip + argc + 2
    return op

add_op = make_arith_op(2, lambda a, b: a + b)
mult_op = make_arith_op(2, lambda a, b: a * b)

input_op = make_arith_op(0, lambda: int(input("input op:")))

less_than_op = make_arith_op(2, lambda a, b: 1 if a < b else 0)
equal_to_op = make_arith_op(2, lambda a, b: 1 if a == b else 0)

def output_op(cells, ip):
    result, = get_operands(cells, ip, 1)
    print(result)
    return ip + 2

def jump_if_true(cells, ip):
    val, target = get_operands(cells, ip, 2)
    if val != 0:
        return target
    return ip + 3

def jump_if_false(cells, ip):
    val, target = get_operands(cells, ip, 2)
    if val == 0:
        return target
    return ip + 3

ops = [
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


def run_comp(cells):
    ip = 0
    while cells[ip] != 99:
        op = cells[ip] % 100
        ip = ops[op](cells, ip)


cells = list(initial_cells)
run_comp(cells)
