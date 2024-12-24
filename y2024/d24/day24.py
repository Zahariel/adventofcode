import operator
from collections import defaultdict

from parsy import seq, string, whitespace, regex

from dag import Dag
from parsing import number, split_on_blank


def parse_input(line):
    return seq(regex(r"...") << string(": "), number).map(tuple).parse(line)

def parse_gate(line):
    return seq(
        regex(r"...") << whitespace,
        regex("AND|OR|XOR") << whitespace,
        regex(r"...") << string(" -> "),
        regex(r"...")
    ).map(tuple).parse(line)

with open("input.txt") as f:
    inputs, gates = split_on_blank(f)
    inputs = [parse_input(i) for i in inputs]
    gates = [parse_gate(g) for g in gates]

OPERATIONS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor
}


input_map = {name: value for name, value in inputs}
ancestors = {output: {left, right} for left, _, right, output in gates}
operations = {output: op for _, op, __, output in gates}

dag = Dag.from_parents(ancestors)

results = dag.propagate_named_values(input_map, lambda node, values: OPERATIONS[operations[node]](*values))

final_outputs = {name: value for name, value in results.items() if name[0] == "z"}

ordered = [str(value) for name, value in sorted(final_outputs.items(), reverse=True)]
print(int("".join(ordered), 2))


# part 2.... what the heck

starting_xors = dict()
other_xors = dict()
ands = defaultdict(set)
ors = defaultdict(set)

for left, op, right, output in gates:
    if op == "XOR":
        if left[0] == "x" or right[0] == "x":
            starting_xors[frozenset({left, right})] = output
        else:
            other_xors[left] = (right, output)
            other_xors[right] = (left, output)
    elif op == "AND":
        ands[left].add((right, output))
        ands[right].add((left, output))
    else:
        ors[left].add((right, output))
        ors[right].add((left, output))

starting_errors = dict()
output_bits = dict()
for wires, mid in starting_xors.items():
    if mid not in other_xors:
        starting_errors[wires] = mid
        print(f"{wires} shouldn't lead to {mid}")
    else:
        output_bits[wires] = (mid, other_xors[mid])

other_errors = dict()
for wires, (mid, (other, output)) in sorted(output_bits.items(), key=lambda i:i[1][1][1]):
    if output[0] != "z":
        print(f"{wires} -> {mid} + {other} -> {output} seems wrong")
        other_errors[wires] = (mid, other, output)

# this just has a different structure, but it's still right
del starting_errors[frozenset({"x00", "y00"})]

# now figure out what they should be
swapped = []

for wires, wrong_target in starting_errors.items():
    swapped.append(wrong_target)
    index = next(iter(wires))[1:]
    candidates = list(ancestors["z"+index])
    for candidate in candidates:
        if operations[candidate] != "OR":
            print(f"{wrong_target} swapped with {candidate}")
            swapped.append(candidate)
    pass

for wires, (mid, other, output) in other_errors.items():
    print(f"inspecting {wires} -> {mid} + {other} -> {output}")
    # i don't think this is guaranteed to be right but it was for all 3 of my cases
    swapped.append(output)
    correct_output = "z" + next(iter(wires))[1:]
    swapped.append(correct_output)

# in theory there could be other kinds of errors, but all four of mine involved XOR outputs

print(",".join(sorted(swapped)))

