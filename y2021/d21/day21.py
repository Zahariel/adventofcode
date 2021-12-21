import re
from collections import defaultdict

def parse(line):
    return int(re.match(r"Player . starting position: (\d)", line.strip()).groups()[0])

with open("input.txt") as f:
    data = [parse(line) for line in f.readlines()]

print(data)


DIE_MAX = 100
SCORE_MAX = 1000
POSITION_MAX = 10
die = 1
die_rolls = 0
player = 0
positions = list(data)
scores = [0 for _ in data]

while all(score < SCORE_MAX for score in scores):
    move = die + (die + 1) + (die + 2)
    die += 3
    die = (die - 1) % DIE_MAX + 1
    die_rolls += 3
    positions[player] += move
    positions[player] = (positions[player] - 1) % POSITION_MAX + 1
    scores[player] += positions[player]
    player += 1
    player %= len(positions)

print(scores)
print(sum(score for score in scores if score < 1000) * die_rolls)

# part 2

p0start = data[0]
p1start = data[1]
multiverse = dict()
multiverse[((p0start, 0), (p1start, 0), 0)] = 1
# multiverse: (p0pos, p0score), (p1pos, p1score), player -> number of universes
DIRAC_3DIE = [0, 0, 0, 1, 3, 6, 7, 6, 3, 1]

p0wins = 0
p1wins = 0

while len(multiverse) > 0:
    new_multiverse = defaultdict(int)
    for val, count in enumerate(DIRAC_3DIE):
        if count == 0: continue
        for ((p0pos, p0score), (p1pos, p1score), player), universes in multiverse.items():
            if player == 0:
                p0pos += val
                p0pos = (p0pos - 1) % POSITION_MAX + 1
                p0score += p0pos
                if p0score >= 21:
                    p0wins += universes * count
                    continue
            else:
                p1pos += val
                p1pos = (p1pos - 1) % POSITION_MAX + 1
                p1score += p1pos
                if p1score >= 21:
                    p1wins += universes * count
                    continue
            new_multiverse[(p0pos, p0score), (p1pos, p1score), 1-player] += universes * count
    multiverse = new_multiverse

print(0, p0wins)
print(1, p1wins)



