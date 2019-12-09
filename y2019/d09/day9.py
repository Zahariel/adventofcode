from y2019.intcode import run_comp, InputFunction

with open("input.txt") as f:
    line = f.readline()

initial_cells = [int(x) for x in line.strip().split(",")]

run_comp(initial_cells, input_fn=InputFunction([1]))
run_comp(initial_cells, input_fn=InputFunction([2]))
