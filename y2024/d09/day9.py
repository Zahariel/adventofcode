import functools


def parse(line):
    return [int(c) for c in line]


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

disk = lines[0]

labeled_disk = [(i // 2 if i % 2 == 0 else None, s) for i, s in enumerate(disk)]

write_ptr = 1
read_ptr = len(labeled_disk) - 1
while write_ptr < read_ptr:
    _, w_size = labeled_disk[write_ptr]
    r_id, r_size = labeled_disk[read_ptr]
    if w_size < r_size:
        # write as much as possible
        labeled_disk[write_ptr] = (r_id, w_size)
        labeled_disk[read_ptr] = (r_id, r_size - w_size)
        write_ptr += 2
    else:
        # write the whole file
        labeled_disk[read_ptr] = (None, r_size)
        labeled_disk[write_ptr:write_ptr+1] = [(r_id, r_size), (None, w_size - r_size)]
        write_ptr += 1
        # implicit read_ptr -= 1 because the list expanded
        read_ptr -= 1

def checksum_labeled(disk):
    def add_file(acc, file):
        s, l = acc
        id, sz = file
        return s if id is None else s + (2 * l + sz - 1) * sz // 2 * id, l + sz
    return functools.reduce(add_file, disk, (0, 0))[0]

print(checksum_labeled(labeled_disk))

# part 2

labeled_disk = [(i // 2 if i % 2 == 0 else None, s) for i, s in enumerate(disk)]

output_disk = labeled_disk[:]

read_ptr = len(labeled_disk) - 1
for id, size in reversed(labeled_disk[::2]):
    # look for a sufficiently big gap
    target = None
    old_spot = None
    for spot, (id2, size2) in enumerate(output_disk):
        if id == id2:
            old_spot = spot
            break
        if target is None and id2 is None and size2 >= size:
            target = spot
    if target is not None:
        # blank out the old file
        output_disk[old_spot] = (None, size)
        # move the file
        free_size = output_disk[target][1]
        output_disk[target:target+1] = [(id, size), (None, free_size - size)]

print(checksum_labeled(output_disk))
