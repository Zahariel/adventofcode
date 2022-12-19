import operator
import re
from functools import reduce

class Blueprint:
    def __init__(self, id, ore_cost, clay_ore, obs_ore, obs_clay, geode_ore, geode_obs):
        self.geode_obs = geode_obs
        self.geode_ore = geode_ore
        self.obs_clay = obs_clay
        self.obs_ore = obs_ore
        self.clay_ore = clay_ore
        self.ore_cost = ore_cost
        self.id = id
        self.memory = dict()

    def __repr__(self):
        return f"Blueprint({self.id}, {self.ore_cost}, {self.clay_ore}, {self.obs_ore}, {self.obs_clay}, {self.geode_ore}, {self.geode_obs})"

    def evaluate(self, time_left, ore_bots, clay_bots, obs_bots, geode_bots, ore, clay, obs, geodes, best, path):
        if time_left == 0:
            # if geodes >= 8: print(geodes, path)
            return geodes
        if (time_left, ore_bots, clay_bots, obs_bots, geode_bots, ore, clay, obs) in self.memory:
            return self.memory[time_left, ore_bots, clay_bots, obs_bots, geode_bots, ore, clay, obs] + geodes
        # if we can't do better by building a geode bot every minute, give up
        if geodes + geode_bots * time_left + (time_left * time_left + time_left) // 2 <= best:
            return geodes + time_left * geode_bots

        possible = [geodes + time_left * geode_bots]
        # can always not build
        possible.append(self.evaluate(time_left - 1, ore_bots, clay_bots, obs_bots, geode_bots, ore + ore_bots, clay + clay_bots, obs + obs_bots, geodes + geode_bots, max(best, max(possible)), path + "-"))
        if ore >= self.ore_cost:
            possible.append(self.evaluate(time_left - 1, ore_bots + 1, clay_bots, obs_bots, geode_bots, ore + ore_bots - self.ore_cost, clay + clay_bots, obs + obs_bots, geodes + geode_bots, max(best, max(possible)), path + "O"))
        if ore >= self.clay_ore:
            possible.append(self.evaluate(time_left - 1, ore_bots, clay_bots + 1, obs_bots, geode_bots, ore + ore_bots - self.clay_ore, clay + clay_bots, obs + obs_bots, geodes + geode_bots, max(best, max(possible)), path + "C"))
        if ore >= self.obs_ore and clay >= self.obs_clay:
            possible.append(self.evaluate(time_left - 1, ore_bots, clay_bots, obs_bots + 1, geode_bots, ore + ore_bots - self.obs_ore, clay + clay_bots - self.obs_clay, obs + obs_bots, geodes + geode_bots, max(best, max(possible)), path + "B"))
        if ore >= self.geode_ore and obs >= self.geode_obs:
            possible.append(self.evaluate(time_left - 1, ore_bots, clay_bots, obs_bots, geode_bots + 1, ore + ore_bots - self.geode_ore, clay + clay_bots, obs + obs_bots - self.geode_obs, geodes + geode_bots, max(best, max(possible)), path + "G"))

        # print(time_left, ore_bots, clay_bots, obs_bots, geode_bots, ore, clay, obs, "->", max(possible) - geodes)
        self.memory[time_left, ore_bots, clay_bots, obs_bots, geode_bots, ore, clay, obs] = max(possible) - geodes
        return max(possible)



def parse(line):
    [blueprint, ore_cost, clay_ore, obs_ore, obs_clay, geode_ore, geode_obs] = re.match(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line).groups()
    return Blueprint(int(blueprint), int(ore_cost), int(clay_ore), int(obs_ore), int(obs_clay), int(geode_ore), int(geode_obs))

with open("input.txt") as file:
    blueprints = [parse(line.rstrip()) for line in file]

print(blueprints)
TIME = 24
results = []
for bp in blueprints:
    result = bp.evaluate(TIME, 1, 0, 0, 0, 0, 0, 0, 0, 0, "")
    print(bp.id, result)
    results.append((bp.id, result))

print(sum(id * result for (id, result) in results))

# part 2
TIME = 32
results = []
for bp in blueprints[:3]:
    result = bp.evaluate(TIME, 1, 0, 0, 0, 0, 0, 0, 0, 0, "")
    print(bp.id, result)
    results.append(result)

print(reduce(operator.mul, results))
