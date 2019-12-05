
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


def add_op(cells, ip):
    a, b = get_operands(cells, ip, 2)
    cells[cells[ip + 3]] = a + b
    return ip + 4

def mult_op(cells, ip):
    a, b = get_operands(cells, ip, 2)
    cells[cells[ip + 3]] = a * b
    return ip + 4

def input_op(cells, ip):
    cells[cells[ip + 1]] = int(input("input op:"))
    return ip + 2

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

def less_than(cells, ip):
    a, b = get_operands(cells, ip, 2)
    if a < b:
        cells[cells[ip + 3]] = 1
    else:
        cells[cells[ip + 3]] = 0
    return ip + 4

def equal_to(cells, ip):
    a, b = get_operands(cells, ip, 2)
    if a == b:
        cells[cells[ip + 3]] = 1
    else:
        cells[cells[ip + 3]] = 0
    return ip + 4

ops = [
    None,
    add_op,
    mult_op,
    input_op,
    output_op,
    jump_if_true,
    jump_if_false,
    less_than,
    equal_to
]


def run_comp(cells):
    ip = 0
    while cells[ip] != 99:
        op = cells[ip] % 100
        ip = ops[op](cells, ip)


cells = list(initial_cells)
run_comp(cells)
