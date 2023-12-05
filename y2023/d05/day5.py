from parsy import regex, seq, string

from parsing import chunks, split_on_blank

def parse_header(line):
    parser = seq(
        regex(r"[^- ]+") << string("-to-"),
        regex(r"[^- ]+") << string(" map:")
    ).map(tuple)
    return parser.parse(line)

def parse_map(map):
    left,right = parse_header(map[0])
    ranges = [tuple(int(num) for num in line.split()) for line in map[1:]]
    return (left, right), [(dest, src, src + size) for dest, src, size in ranges]

with open("input.txt") as file:
    groups = list(split_on_blank(file))

    seeds = [int(s) for s in groups[0][0].split()[1:]]

    maps = dict(parse_map(map) for map in groups[1:])

def lookup(val, map):
    for dest, start, end in map:
        if start <= val < end:
            return dest + (val - start)
    return val
def lookup_chain(val):
    for (left, right), map in maps.items():
        val = lookup(val, map)
    return val

print(min(lookup_chain(seed) for seed in seeds))


# part 2, yikes
seed_ranges = [(start, start + size) for [start, size] in chunks(seeds, 2)]

def translate_range(range, map):
    results = []
    needs_translated = [range]
    while len(needs_translated) > 0:
        start, end = needs_translated.pop()
        for dest, src_start, src_end in map:
            if src_start <= start < src_end:
                # start is within this range
                if end < src_end:
                    # whole processable range within this one
                    results.append((dest + (start - src_start), dest + (end - src_start)))
                    break
                else:
                    # need to process high half later
                    new_start = src_end
                    results.append((dest + (start - src_start), dest + (src_end - src_start)))
                    needs_translated.append((new_start, end))
                    break
            elif start < src_start and src_start < end:
                if end < src_end:
                    # need to process low half later
                    new_end = src_start
                    results.append((dest, dest + (end - src_start)))
                    needs_translated.append((start, new_end))
                    break
                else:
                    # need to split current
                    results.append((dest, dest + (src_end - src_start)))
                    needs_translated.append((start, src_start))
                    needs_translated.append((src_end, end))
                    break
        else:
            # didn't hit any range
            results.append((start, end))

    return results

ranges = seed_ranges[:]
for (left, right), map in maps.items():
    new_ranges = []
    for range in ranges:
        new_ranges += translate_range(range, map)
    ranges = new_ranges

print(min(start for start, end in ranges))
