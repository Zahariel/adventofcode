

ROCK = 0
PAPER = 1
SCISSORS = 2

values = {
    'A': ROCK,
    'B': PAPER,
    'C': SCISSORS,
    'X': ROCK,
    'Y': PAPER,
    'Z': SCISSORS
}

with open("input.txt") as lines:
    games = [(values[line[0]], values[line[2]]) for line in lines]

print(games)

def score(game):
    they, me = game
    result = ((me - they + 1) % 3) * 3
    return result + me + 1

print([score(game) for game in games])
print(sum(score(game) for game in games))

def score2(game):
    they, result = game
    me = ((they + result - 1) % 3)
    return result * 3 + me + 1
print([score2(game) for game in games])
print(sum(score2(game) for game in games))
