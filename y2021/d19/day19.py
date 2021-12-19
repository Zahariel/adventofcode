import itertools
from collections import Counter

def parse(line):
    x, y, z = line.strip().split(",")
    return int(x), int(y), int(z)

with open("input.txt") as f:
    scanners = []
    beacons = []
    for line in f.readlines():
        if len(line.strip()) == 0:
            scanners.append(beacons)
            beacons = []
        elif line.startswith("---"):
            continue
        else:
            beacons.append(parse(line))

print(len(scanners), "scanners")

def vector_add(v1, v2):
    return tuple(l + r for l, r in zip(v1, v2))

def vector_diff(v1, v2):
    return tuple(l - r for l, r in zip(v1, v2))

def vector_neg(v):
    return tuple(-n for n in v)

# x, negx, y, negy, z, negz: inverse orientation
ORIENTATIONS = {
    (0, 1, 1, 1, 2, 1): (0, 1, 1, 1, 2, 1),
    (1, 1, 2, 1, 0, 1): (2, 1, 0, 1, 1, 1),
    (2, 1, 0, 1, 1, 1): (1, 1, 2, 1, 0, 1),

    (0, -1, 1, -1, 2, 1): (0, -1, 1, -1, 2, 1),
    (1, -1, 2, 1, 0, -1): (2, -1, 0, -1, 1, 1),
    (2, 1, 0, -1, 1, -1): (1, -1, 2, -1, 0, 1),

    (0, -1, 1, 1, 2, -1): (0, -1, 1, 1, 2, -1),
    (1, 1, 2, -1, 0, -1): (2, -1, 0, 1, 1, -1),
    (2, -1, 0, -1, 1, 1): (1, -1, 2, 1, 0, -1),

    (0, 1, 1, -1, 2, -1): (0, 1, 1, -1, 2, -1),
    (1, -1, 2, -1, 0, 1): (2, 1, 0, -1, 1, -1),
    (2, -1, 0, 1, 1, -1): (1, 1, 2, -1, 0, -1),

    (0, -1, 2, 1, 1, 1): (0, -1, 2, 1, 1, 1),
    (2, 1, 1, 1, 0, -1): (2, -1, 1, 1, 0, 1),
    (1, 1, 0, -1, 2, 1): (1, -1, 0, 1, 2, 1),

    (0, 1, 2, -1, 1, 1): (0, 1, 2, 1, 1, -1),
    (2, -1, 1, 1, 0, 1): (2, 1, 1, 1, 0, -1),
    (1, 1, 0, 1, 2, -1): (1, 1, 0, 1, 2, -1),

    (0, 1, 2, 1, 1, -1): (0, 1, 2, -1, 1, 1),
    (2, 1, 1, -1, 0, 1): (2, 1, 1, -1, 0, 1),
    (1, -1, 0, 1, 2, 1): (1, 1, 0, -1, 2, 1),

    (0, -1, 2, -1, 1, -1): (0, -1, 2, -1, 1, -1),
    (2, -1, 1, -1, 0, -1): (2, -1, 1, -1, 0, -1),
    (1, -1, 0, -1, 2, -1): (1, -1, 0, -1, 2, -1),
}

def apply_orientation(ori, v):
    return v[ori[0]]*ori[1], v[ori[2]]*ori[3], v[ori[4]]*ori[5]

def chain_orientation(first, second):
    return (second[first[0]*2], second[first[0]*2+1]*first[1],
            second[first[2]*2], second[first[2]*2+1]*first[3],
            second[first[4]*2], second[first[4]*2+1]*first[5])

def could_be_same(v1, v2):
    for ori in ORIENTATIONS:
        if v1 == apply_orientation(ori, v2):
            return ori
    return None

def relate(left, right):
    relationships = []
    for left1, left2 in itertools.combinations(left, 2):
        left_vec = vector_diff(left1, left2)
        for right1, right2 in itertools.permutations(right, 2):
            right_vec = vector_diff(right1, right2)
            result = could_be_same(left_vec, right_vec)
            if result is not None:
                relationships.append((left1, left2, right1, right2, result))

    if len(relationships) == 0: return None, None
    found = Counter(rel[4] for rel in relationships)
    [(true_rel, count)] = found.most_common(1)
    # need at least 12 commmon beacons: (12 * 11)/2 = 66 common differences
    if count < 66: return None, None
    # delete any red herrings
    relationships = [rel for rel in relationships if rel[4] == true_rel]
    left_beacon, _, right_beacon, _, _ = relationships[0]
    return vector_diff(left_beacon, apply_orientation(true_rel, right_beacon)), true_rel

# this takes about 10 minutes, so i saved the result after the first time i got the right answer
# relationships = [{(idx, (0,0,0), (0,1,1,1,2,1))} for idx in range(len(scanners))]
# for left, right in itertools.combinations(range(len(scanners)), 2):
#     pos, ori = relate(scanners[left], scanners[right])
#     if pos is not None:
#         print(left, right, pos, ori)
#         relationships[left].add((right, pos, ori))
#         relationships[right].add((left, apply_orientation(ORIENTATIONS[ori], vector_neg(pos)), ORIENTATIONS[ori]))

with open("saved_rels.txt") as f:
    relationships = [eval(line.strip().partition(" ")[2]) for line in f.readlines()]

print("=====")
for idx, rels in enumerate(relationships):
    print(idx, rels)
print("=====")

# if a and b are related as pos, ori, then all beacons k in b are seen by a at pos + apply(ori, k)
def merge_into(current, new, pos, ori):
    for beacon in new:
        current.add(vector_add(pos, apply_orientation(ori, beacon)))

collapsed = set()
def collapse_scanners(idx, studying):
    if idx in collapsed: return
    added = set()
    studying.add(idx)
    for other, pos, rel in relationships[idx]:
        if other in studying: continue
        collapse_scanners(other, studying)
        added |= set((third, vector_add(pos, apply_orientation(rel, tpos)), chain_orientation(rel, trel)) for third, tpos, trel in relationships[other])
    studying.remove(idx)
    relationships[idx] |= added
    collapsed.add(idx)


collapse_scanners(0, set())
print(relationships[0])

all_beacons = set()
for idx, pos, rel in relationships[0]:
    merge_into(all_beacons, scanners[idx], pos, rel)

print(len(all_beacons))

# part 2
def manhattan_length(v):
    return sum(abs(x) for x in v)

print(max(manhattan_length(vector_diff(v1, v2)) for (_, v1, _), (_, v2, _) in itertools.combinations(relationships[0], 2)))
