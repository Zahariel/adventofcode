import re

from collections import defaultdict

class Chemical:
    def __init__(self, line):
        inputs, amount, name = re.match(r"(.*) => (\d*) ([A-Z]*)", line.rstrip()).groups()
        self.amount = int(amount)
        self.name = name
        self.inputs = []
        self.used = 0
        self.created = 0
        if len(inputs) > 0:
            for input in inputs.split(", "):
                input_amount, input_name = re.match(r"(\d*) ([A-Z]*)", input.strip()).groups()
                self.inputs.append((int(input_amount), input_name))

    @property
    def unused(self):
        return self.created - self.used

    def __str__(self):
        return "(%d/%d) %d %s <= %s" % (self.used, self.created, self.amount, self.name, self.inputs)

def parse_input():
    with open("input.txt") as f:
        all_chems = [Chemical(line) for line in f]
    chems = {chem.name: chem for chem in all_chems}
    # add ORE, which can be created for free
    chems["ORE"] = Chemical(" => 1 ORE")
    return chems

factory = parse_input()

def make_chem(factory, amount_needed, name):
    chems_needed = defaultdict(int)
    chems_needed[name] = amount_needed

    while len(chems_needed) > 0:
        # print(chems_needed)
        product_name, amount = chems_needed.popitem()
        chem = factory[product_name]
        if chem.unused < amount:
            batches = (amount - chem.unused - 1) // chem.amount + 1
            for (input_amount, input_name) in chem.inputs:
                chems_needed[input_name] = chems_needed[input_name] + input_amount * batches
            chem.created = chem.created + chem.amount * batches
        chem.used = chem.used + amount

make_chem(factory, 1, "FUEL")
ore_per_fuel = factory["ORE"].created
print(ore_per_fuel)

factory = parse_input()
# add 1_000_000_000_000 ore
INITIAL_ORE = 1_000_000_000_000
factory["ORE"].created = INITIAL_ORE

while factory["ORE"].created == INITIAL_ORE:
    ore_remaining = factory["ORE"].unused
    # eventually this will get down to making one at a time, but start with big batches for performance
    make_chem(factory, ore_remaining // (ore_per_fuel * 3) + 1, "FUEL")
    print(factory["FUEL"].created, factory["ORE"].unused)

print(factory["FUEL"].created - 1)

