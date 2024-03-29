import functools

import parsing

def parse(line):
    return eval(line)

with open("input.txt") as file:
    groups = [tuple(group) for group in parsing.split_on_blank(file, line_parser=parse)]


print(groups)

# part 1
def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        if l < r: return -1
        if l > r: return 1
        return 0
    if isinstance(l, list) and isinstance(r, list):
        if len(l) == 0 and len(r) == 0: return 0
        if len(l) == 0: return -1
        if len(r) == 0: return 1
        subresult = compare(l[0], r[0])
        if subresult != 0:
            return subresult
        return compare(l[1:], r[1:])
    if isinstance(l, int):
        return compare([l], r)
    return compare(l, [r])

acc = 0
for i, (l, r) in enumerate(groups):
    if compare(l, r) < 0:
        print(l, "<", r)
        acc += i + 1
    else:
        print(l, ">", r)
print(acc)


# part 2

packets = [packet for group in groups for packet in group]
packets.append([[2]])
packets.append([[6]])

sorted_packets = sorted(packets, key=functools.cmp_to_key(compare))

print(sorted_packets)

idx_2 = sorted_packets.index([[2]])+1
idx_6 = sorted_packets.index([[6]])+1
print(idx_2, idx_6, idx_2 * idx_6)
