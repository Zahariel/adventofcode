from y2019.intcode import AsciiComp
with open("input.txt") as f:
    initial_cells = [int(c) for c in f.readline().strip().split(",")]

def listify(string):
    result = [ord(c) for c in string]
    result.append(10)
    return result

inputs = [
    "NOT T T",
    "AND A T",
    "AND B T",
    "AND C T",
    "NOT T J",
    "AND D J",
    "WALK"
]
new_comp = AsciiComp(initial_cells, inputs)
new_comp.run()


inputs = [
    "NOT T T",
    "AND A T",
    "AND B T",
    "AND C T",
    "NOT T J",
    "AND D J",
    # J is "a pit is coming up, i want to jump"
    "NOT E T",
    "NOT T T",
    "OR H T",
    "AND T J",
    "RUN"
]

new_comp = AsciiComp(initial_cells, inputs)
new_comp.run()

