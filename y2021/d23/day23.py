import breadth_first

TARGETS = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

RIGHT_WALL = 11

def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

class State:
    def __init__(self, slugs, room_depth, history):
        self.slugs = frozenset(slugs)
        self.room_depth = room_depth
        self.history = history

    def is_solved(self, cost):
        if all(x == TARGETS[c] for c, x, _ in self.slugs): return cost, self.history
        return None

    def move_to(self, kind, x1, y1, x2, y2):
        return manhattan(x1, y1, x2, y2) * COSTS[kind], State(self.slugs ^ {(kind, x1, y1), (kind, x2, y2)}, self.room_depth, self.history + [(kind, x1, y1, x2, y2)])

    def moves(self):
        moves = []
        for kind, x, y in self.slugs:
            if y == 0:
                # slug is in the corridor; can only move to its final target, if it can get there
                target = TARGETS[kind]
                # first check that the target room is acceptably populated
                if any(x2 == target and kind2 != kind for kind2, x2, _ in self.slugs): continue
                # next check that the path is clear
                if any(y2 == 0 and (target < x2 < x or x < x2 < target) for _, x2, y2 in self.slugs): continue
                # move as far into the room as possible
                populace = {y2 for _, x2, y2 in self.slugs if x2 == target}
                target_y = min(populace)-1 if len(populace) > 0 else self.room_depth
                moves.append(self.move_to(kind, x, y, target, target_y))
            else:
                # if we're trapped in, give up
                if any(x2 == x and y2 < y for _, x2, y2 in self.slugs): continue
                # figure out where in the corridor we can get to
                left = x
                right = x+1
                while left > 0 and not any (x2 == left - 1 and y2 == 0 for _, x2, y2 in self.slugs):
                    left -= 1
                while right < 11 and not any (x2 == right and y2 == 0 for _, x2, y2 in self.slugs):
                    right += 1
                for target in range(left, right):
                    # skip squares in front of rooms
                    if target in TARGETS.values(): continue
                    moves.append(self.move_to(kind, x, y, target, 0))
        return moves

    def __hash__(self):
        return hash(self.slugs)

    def __eq__(self, other):
        return self.slugs == other.slugs

    def __str__(self):
        return str(self.slugs)

    def __lt__(self, other):
        # i don't think this has to be compatible with __eq__
        return 0

with open("input.txt") as f:
    f.readline()
    locs = []
    for y, line in enumerate(f.readlines()):
        for x, c in enumerate(line.rstrip()):
            if c not in {"#", ".", " "}:
                locs.append((c, x-1, y))
    initial = State(locs, 2, [])

print(initial)

result = breadth_first.breadth_first(initial, neighbors_fn=lambda s: s.moves(), process_fn=lambda c,s: s.is_solved(c))
print(result)

# part 2
extra_rows = ["  #D#C#B#A#","  #D#B#A#C#"]
with open("input.txt") as f:
    f.readline()
    locs = []
    lines = list(f.readlines())
    # add the nonsense
    lines[2:2] = extra_rows
    for y, line in enumerate(lines):
        for x, c in enumerate(line.rstrip()):
            if c not in {"#", ".", " "}:
                locs.append((c, x-1, y))
    initial = State(locs, 4, [])

print(initial)
result = breadth_first.breadth_first(initial, neighbors_fn=lambda s: s.moves(), process_fn=lambda c,s: s.is_solved(c))
print(result)
