import re
from collections import defaultdict

def parse(line):
    line = line.split(": ")[1]
    return [[re.match(r"(\d+) (.+)", color).groups() for color in draw.split(", ")] for draw in line.split("; ")]


with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]

MAXIMA = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def check_game(game):
    return all(amt <= MAXIMA[color] for draw in game for amt, color in draw)

print(sum(n+1 for n, game in enumerate(lines) if check_game(game)))


def power_game(game):
    requirements = defaultdict(int)
    for draw in game:
        for amt, color in draw:
            if requirements[color] < int(amt):
                requirements[color] = int(amt)
    return requirements['red'] * requirements['green'] * requirements['blue']

print(sum(power_game(game) for game in lines))
