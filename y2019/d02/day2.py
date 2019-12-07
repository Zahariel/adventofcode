
with open("input.txt") as f:
    line = f.readline()

initial_cells = [int(x) for x in line.split(",")]

def run_comp(cells):
    pc = 0
    while cells[pc] != 99:
        if cells[pc] == 1:
            cells[cells[pc + 3]] = cells[cells[pc + 1]] + cells[cells[pc + 2]]
            pc = pc + 4
        elif cells[pc] == 2:
            cells[cells[pc + 3]] = cells[cells[pc + 1]] * cells[cells[pc + 2]]
            pc = pc + 4
        else:
            print("unknown opcode ", cells[pc])


TARGET = 19690720

for noun in range(100):
    print(noun)
    for verb in range(100):
        cells = list(initial_cells)
        cells[1] = noun
        cells[2] = verb
        run_comp(cells)
        if cells[0] == TARGET:
            print(100 * noun + verb)
            exit(0)
