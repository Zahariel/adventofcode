from collections import defaultdict

from parsy import regex, seq, string, whitespace

def parse(line):
    name = regex(r"\w{3}")
    parser = seq(name << string(": "),
                 name.sep_by(whitespace)
    ).map(tuple)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

connections = defaultdict(set)
for start, targets in lines:
    for target in targets:
        connections[start].add(target)
        connections[target].add(start)


def get_outward_edges(part):
    result = defaultdict(int)
    for node in part:
        for conn in connections[node] - part:
            result[conn] += 1
    return result


# at each step, try to add the node with the most connections to the current part
# i am outright astonished that this actually worked
def expand(part):
    if len(part) == len(connections): return None
    neigbhors = get_outward_edges(part)
    if sum(neigbhors.values()) == 3:
        return part
    sorted_neighbors = sorted(neigbhors.items(), key=lambda i: -i[1])
    for n,c in sorted_neighbors:
        new_part = part | {n}
        result = expand(new_part)
        if result:
            return result
    return None

result = expand({lines[0][0]})

print(len(result) * (len(connections) - len(result)))
