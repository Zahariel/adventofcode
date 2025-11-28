import functools
import operator
from collections import defaultdict
from time import perf_counter

from parsy import seq, string, regex


def parse(line):
    return seq(regex(r"..") << string("-"), regex(r"..")).map(tuple).parse(line)


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

connections = defaultdict(set)
for left, right in lines:
    connections[left].add(right)
    connections[right].add(left)

def find_triads():
    result = set()
    for start, middles in connections.items():
        for middle in middles:
            for end in connections[middle]:
                if end in middles:
                    result.add(frozenset({start, middle, end}))

    return result

start = perf_counter()

triads = find_triads()
# print(triads)

print(sum(1 for triad in triads if any(n[0] == "t" for n in triad)))

# part 2

def expand(cliques:set[frozenset[str]]):
    result = set()
    for clique in cliques:
        candidates = functools.reduce(operator.and_, (connections[n] for n in clique))
        for candidate in candidates:
            result.add(frozenset(clique | {candidate}))
    return result

cliques = triads
size = 3
biggest = set()
while cliques:
    # print(size, len(cliques))
    next_step = expand(cliques)
    size += 1
    if not next_step:
        # can't expand any more
        biggest = next(iter(cliques))
        break
    cliques = next_step

print(",".join(sorted(biggest)))

soln_1 = perf_counter()

# alternate part 2, based on the Bron-Kerbosch algorithm from wikipedia
#
# algorithm BronKerbosch2(R, P, X) is
#     if P and X are both empty then
#         report R as a maximal clique
#     choose a pivot vertex u in P ⋃ X
#     for each vertex v in P \ N(u) do
#         BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
#         P := P \ {v}
#         X := X ⋃ {v}
#

def find_maximal_cliques(growing:set[str], possibilities:set[str], eliminated:set[str]):
    if not possibilities and not eliminated:
        yield frozenset(growing)
        return
    pivot = next(iter(possibilities | eliminated))
    for node in possibilities - connections[pivot]:
        yield from find_maximal_cliques(growing | {node}, possibilities & connections[node], eliminated & connections[node])
        possibilities.discard(node)
        eliminated.add(node)

# this doesn't actually need to be put into a set() because i'm only using it once, but it makes me nervous to
# leave a bare iterator lying around
max_cliques = set(find_maximal_cliques(set(), set(connections.keys()), set()))

biggest = max(max_cliques, key=len)
print(",".join(sorted(biggest)))

soln_2 = perf_counter()
print(soln_1 - start, soln_2 - soln_1)
# typical results: 1500 ms for my solution, 3 ms for Bron-Kerbosch. ouch
