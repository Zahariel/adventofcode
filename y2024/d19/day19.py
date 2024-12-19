import functools
from time import perf_counter

from parsy import string, regex

from parsing import split_on_blank


def parse_patterns(line):
    return regex(r"[rgbuw]+").sep_by(string(", ")).parse(line)


with open("input.txt") as f:
    patterns, designs = split_on_blank(f)
    patterns = parse_patterns(patterns[0])

start = perf_counter()

pattern_trie = dict()
for p in patterns:
    current = pattern_trie
    for c in p:
        if c not in current:
            current[c] = dict()
        current = current[c]
    current["PATTERN"] = p

# functools.cache is cheating here but i don't care
@functools.cache
def calc_design(design, ptr):
    if ptr == len(design): return 1
    result = 0
    trie_ptr = pattern_trie
    for here in range(ptr, len(design) + 1):
        if "PATTERN" in trie_ptr:
            result += calc_design(design, here)
        if here == len(design): break
        if design[here] not in trie_ptr: break
        trie_ptr = trie_ptr[design[here]]
    return result


ways = [calc_design(d, 0) for d in designs]
print(sum(1 for w in ways if w > 0))
print(sum(ways))

soln_1 = perf_counter()
print(soln_1 - start)

# a different solution that just uses a set. it's disappointing that this is 8x faster than the trie approach

patterns = set(patterns)

@functools.cache
def calc_design2(design, ptr):
    if ptr == len(design): return 1
    return sum(calc_design(design, end) for end in range(ptr, len(design) + 1) if design[ptr:end] in patterns)

ways = [calc_design2(d, 0) for d in designs]
print(sum(1 for w in ways if w > 0))
print(sum(ways))
soln_2 = perf_counter()
print(soln_2 - soln_1)
