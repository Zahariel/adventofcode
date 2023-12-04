from collections import defaultdict

from parsy import regex, seq, string, whitespace

from parsing import number

def parse(line):
    color = seq(
        number << whitespace,
        regex(r"red|green|blue")
    ).map(tuple)

    parser = seq(
        string("Game ") >> number << string(": "),
        color.sep_by(string(", ")).sep_by(string("; "))
    ).map(tuple)
    return parser.parse(line)

with open("input.txt") as file:
    games = [parse(line.rstrip()) for line in file]


MAXIMA = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def check_game(game):
    return all(amt <= MAXIMA[color] for draw in game for amt, color in draw)

print(sum(n for n, game in games if check_game(game)))


def power_game(game):
    requirements = defaultdict(int)
    for draw in game:
        for amt, color in draw:
            if requirements[color] < amt:
                requirements[color] = amt
    return requirements['red'] * requirements['green'] * requirements['blue']

print(sum(power_game(game) for _, game in games))
