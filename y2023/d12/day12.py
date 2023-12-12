from parsy import regex, seq, string, whitespace

from parsing import number

def parse(line):
    springs = regex(r"[#.?]").many()
    counts = number.sep_by(string(","))
    parser = seq(springs << whitespace, counts).map(tuple)
    return parser.parse(line)

with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

print(lines)

MEMO = dict()
def count_ways_inner(original, i, target, j):
    if (i, j) in MEMO:
        return MEMO[i, j]
    if j == len(target):
        return 1 if not(any(cell == '#' for cell in original[i:])) else 0
    if sum(n + 1 for n in target[j:]) > len(original) - i + 1:
        # there's just not enough room left
        return 0
    need_to_place = target[j]
    acc = 0
    for start in range(i, len(original) - need_to_place + 1):
        if start > 0 and original[start-1] == '#':
            # can't skip known-broken springs
            break
        if any(s == '.' for s in original[start:start+need_to_place]):
            # known-good spring in the way
            continue
        if start + need_to_place < len(original) and original[start + need_to_place] == '#':
            # known-broken spring on the end
            continue
        acc += count_ways_inner(original, start + need_to_place + 1, target, j + 1)
    MEMO[i, j] = acc
    return acc

def count_ways(original, i, target, j):
    MEMO.clear()
    return count_ways_inner(original, i, target, j)

print(sum(count_ways(springs, 0, target, 0) for (springs, target) in lines))

print(sum(count_ways(((springs + ['?']) * 5)[:-1], 0, target * 5, 0) for springs, target in lines))

