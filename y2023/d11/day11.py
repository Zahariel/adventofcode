import operator
from functools import reduce

from coord_utils import manhattan

with open("input.txt") as file:
    raw_map = {r: {c for c, cell in enumerate(line) if cell == '#'} for r, line in enumerate(file)}


def expand_rows(galaxies:dict, expansion=1):
    top = min(galaxies.keys())
    bottom = max(galaxies.keys())

    result = dict()
    offset = 0
    for r in range(top, bottom+1):
        if not galaxies[r]:
            offset += expansion-1
        else:
            result[r+offset] = galaxies[r]

    return result

def expand_cols(galaxies:dict, expansion=1):
    left = min(min(row) for row in galaxies.values() if row)
    right = max(max(row) for row in galaxies.values() if row)

    expansion_targets = set(range(left, right+1)) - reduce(operator.or_, galaxies.values())

    result = dict()
    for r in galaxies:
        new_row = set()
        offset = 0
        for c in range(left, right+1):
            if c in galaxies[r]:
                new_row.add(c + offset)
            elif c in expansion_targets:
                offset += expansion-1
        result[r] = new_row

    return result

expanded = expand_rows(expand_cols(raw_map))

final_galaxies = [(r, c) for r, row in expanded.items() for c in row]
print(sum(manhattan(final_galaxies[i], final_galaxies[j]) for i, coords1 in enumerate(final_galaxies) for j, coords2 in enumerate(final_galaxies) if i < j))


# part 2
expanded = expand_rows(expand_cols(raw_map, 1_000_000), 1_000_000)
final_galaxies = [(r, c) for r, row in expanded.items() for c in row]
print(sum(manhattan(final_galaxies[i], final_galaxies[j]) for i, coords1 in enumerate(final_galaxies) for j, coords2 in enumerate(final_galaxies) if i < j))
