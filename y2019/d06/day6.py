from keyeddefaultdict import KeyedDefaultdict

class Planet:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

all_planets = KeyedDefaultdict(Planet)

def parse(line):
    primary, satellite = line.strip().split(")")
    all_planets[primary].children.append(all_planets[satellite])
    all_planets[satellite].parent = all_planets[primary]

with open("input.txt") as f:
    for l in f:
        parse(l)

def resolve_depths(planet, depth):
    planet.depth = depth
    for satellite in planet.children:
        resolve_depths(satellite, depth+1)

star = all_planets["COM"]
resolve_depths(star, 0)

print(sum(planet.depth for planet in all_planets.values()))

def calc_parents(thing):
    if thing == None: return []
    return calc_parents(thing.parent) + [thing.name]

my_parents = calc_parents(all_planets["YOU"])
santa_parents = calc_parents(all_planets["SAN"])

common = 0
while my_parents[common] == santa_parents[common]:
    common = common + 1

print(len(my_parents) + len(santa_parents) - 2 * common - 2)
