import operator
from functools import reduce

import portion
from parsy import regex, seq, string

from parsing import chunks, split_on_blank

class IntInterval(portion.AbstractDiscreteInterval):
    _step = 1

P = portion.create_api(IntInterval)

def parse_header(line):
    parser = seq(
        regex(r"[^- ]+") << string("-to-"),
        regex(r"[^- ]+") << string(" map:")
    ).map(tuple)
    return parser.parse(line)

def parse_map(map):
    left,right = parse_header(map[0])
    ranges = [tuple(int(num) for num in line.split()) for line in map[1:]]
    return (left, right), [(dest-src, P.closedopen(src, src+size)) for dest, src, size in ranges]

with open("input.txt") as file:
    groups = list(split_on_blank(file))

    seeds = [int(s) for s in groups[0][0].split()[1:]]

    maps = dict(parse_map(map) for map in groups[1:])


def lookup(val, map):
    for offset, interval in map:
        if val in interval:
            return val + offset
    return val

def lookup_chain(val):
    for (left, right), map in maps.items():
        val = lookup(val, map)
    return val

print(min(lookup_chain(seed) for seed in seeds))


# part 2
seed_ranges = reduce(operator.or_, (P.closedopen(start, start + size) for [start, size] in chunks(seeds, 2)))

def convert_interval(start, map):
    result = P.empty()
    for offset, interval in map:
        result |= (start & interval).apply(lambda x: x.replace(lower=lambda v: v+offset, upper=lambda v: v+offset))
        start -= interval
    # include anything left over verbatim
    result |= start
    return result

for (left, right), map in maps.items():
    seed_ranges = convert_interval(seed_ranges, map)

print(seed_ranges.lower)


