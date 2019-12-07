from y2019.intcode import run_comp

with open("input.txt") as f:
    line = f.readline()

initial_cells = [int(x) for x in line.split(",")]

cells = list(initial_cells)
run_comp(cells)
