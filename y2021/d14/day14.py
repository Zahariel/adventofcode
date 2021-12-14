import re
from collections import Counter

def parse(line):
    [location, addition] = re.match(r"(..) -> (.)", line.strip()).groups()
    return location, addition

with open("input.txt") as f:
    start = list(f.readline().strip())
    f.readline()
    lines = f.readlines()
    insertions = dict(parse(line) for line in lines)

print("".join(start))
print(insertions)

def digraphs(polymer):
    return ["".join(polymer[i:i+2]) for i in range(len(polymer) - 1)]

def process(base_counts, digraph_counts, insertions):
    base_result = Counter(base_counts)
    digraphs_result = Counter(digraph_counts)
    for digraph, amt in digraph_counts.items():
        if digraph in insertions:
            base = insertions[digraph]
            base_result[base] += amt
            l_di = f"{digraph[0]}{base}"
            r_di = f"{base}{digraph[1]}"
            digraphs_result[l_di] += amt
            digraphs_result[r_di] += amt
            digraphs_result[digraph] -= amt
    return base_result, digraphs_result

STEPS = 40
base_counts = Counter(start)
digraph_counts = Counter(digraphs(start))
for i in range(STEPS):
    base_counts, digraph_counts = process(base_counts, digraph_counts, insertions)
    print("=====", i+1, "=====")
    print(base_counts)
    amts_sorted = sorted(base_counts.values())
    print(amts_sorted[-1] - amts_sorted[0])

