import re

class Group:
    def __init__(self, team, size, hp, damage, type, immunities, weaknesses, initiative):
        self.team = team
        self.size = size
        self.hp = hp
        self.damage = damage
        self.type = type
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.initiative = initiative

    def effective_power(self):
        return self.size * self.damage

    def attack_order_sort(self):
        return self.effective_power(), self.initiative

    def damage_taken(self, attacker):
        if attacker.type in self.immunities: return 0
        power = attacker.effective_power()
        if attacker.type in self.weaknesses: return power * 2
        return power

    def hurt_by(self, attacker):
        # print(attacker, "attacks", self, end=" ")
        damage = self.damage_taken(attacker)
        casualties = damage // self.hp
        self.size -= casualties
        if self.size < 0:
            self.size = 0
        # print("dealing", damage, "for", casualties, "leaving", self.size)

    def __repr__(self):
        return "Group(%d, %d, %d, %s, %s, %s, %s, %d)" % (self.team, self.size, self.hp, self.damage, self.type, repr(self.immunities), repr(self.weaknesses), self.initiative)

def parse_mod(match):
    if match is None: return []
    group = match.group(1)
    return group.split(", ")

def parse_line(line, team):
    size, hp, mods, attack, type, initiative = re.match(r"(\d+) units each with (\d+) hit points \((.*)\) with an attack that does (\d+) (\S+) damage at initiative (\d+)", line).groups()
    weaknesses_match = re.search(r"weak to ([^;]*)(;|$)", mods)
    immunities_match = re.search(r"immune to ([^;]*)(;|$)", mods)
    weaknesses = parse_mod(weaknesses_match)
    immunities = parse_mod(immunities_match)
    return Group(team, int(size), int(hp), int(attack), type, immunities, weaknesses, int(initiative))

def choose_targets(units):
    targets = [-1 for _ in units]
    under_attack = set()
    for i, attacker in enumerate(units):
        victim = -1
        victim_damage = 0
        for j, defender in enumerate(units):
            if defender.team == attacker.team: continue
            if j in under_attack: continue
            damage = defender.damage_taken(attacker)
            if damage > victim_damage:
                victim_damage = damage
                victim = j
        targets[i] = victim
        under_attack.add(victim)
    return targets

boost = 0
while True:
    boost += 1
    if boost % 1 == 0: print(boost)
    with open("day24input.txt") as file:
        file.readline()
        line = file.readline().strip()
        immune_system = []
        while len(line) > 0:
            immune_system.append(parse_line(line, 0))
            line = file.readline().strip()
        file.readline()
        line = file.readline().strip()
        invaders = []
        while len(line) > 0:
            invaders.append(parse_line(line, 1))
            line = file.readline().strip()
    # print(immune_system)
    # print(invaders)
    # print()

    # boost immune system
    for group in immune_system:
        group.damage += boost

    while len(immune_system) > 0 and len(invaders) > 0:
        all_units = immune_system + invaders
        all_units.sort(key=Group.attack_order_sort, reverse=True)

        targets = choose_targets(all_units)
        if all(target == -1 for target in targets):
            print("stalemate at", boost)
            break
        attacks = list(zip(all_units, targets))
        attacks.sort(key=lambda p: p[0].initiative, reverse=True)
        for attacker, target in attacks:
            if target == -1: continue
            all_units[target].hurt_by(attacker)

        immune_system = [u for u in immune_system if u.size > 0]
        invaders = [u for u in invaders if u.size > 0]
        # print(immune_system)
        # print(invaders)
        # print()

    if len(invaders) == 0: break

print(boost)
print(sum(u.size for u in immune_system) + sum(u.size for u in invaders))