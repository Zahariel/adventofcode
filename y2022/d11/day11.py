import functools
import operator

import parsing

class Monkey:
    def __init__(self, defn):
        self.id = int(defn[0].split()[1][:-1])
        self.inventory = [int(thing.rstrip(",")) for thing in defn[1].split()[2:]]
        self.operation = defn[2].split()[4]
        self.operand = defn[2].split()[5]
        self.test = int(defn[3].split()[-1])
        self.true_target = int(defn[4].split()[-1])
        self.false_target = int(defn[5].split()[-1])

    def inspect(self, item, total_modulus):
        if self.operand == "old":
            temp_oper = item
        else:
            temp_oper = int(self.operand)
        if self.operation == "+":
            return (item + temp_oper) % total_modulus
        else:
            return (item * temp_oper) % total_modulus

    def target(self, item):
        if item % self.test == 0:
            return self.true_target
        else:
            return self.false_target

    def __repr__(self):
        return f"Monkey({self.id}, {self.inventory}, {self.operation} {self.operand}, {self.test} -> {self.true_target} / {self.false_target}"

# part 1
with open("input.txt") as file:
    sections = parsing.split_on_blank(file)
    monkeys = [Monkey(section) for section in sections]

print(monkeys)
inspections = [0] * len(monkeys)

total_modulus = functools.reduce(operator.mul, (monkey.test for monkey in monkeys))


def take_turn(index, worry_reduction):
    monkey = monkeys[index]
    for item in monkey.inventory:
        result = monkey.inspect(item, total_modulus) // worry_reduction
        target = monkey.target(result)
        monkeys[target].inventory.append(result)
    inspections[index] += len(monkey.inventory)
    monkey.inventory = []

for i in range(20):
    for index in range(len(monkeys)):
        take_turn(index, 3)
    print("round", i)
    print(monkeys)
    print(inspections)

sorted_inspections = sorted(enumerate(inspections), key=lambda p: p[1])
print(sorted_inspections)
print(sorted_inspections[-1][1] * sorted_inspections[-2][1])

# part 2
with open("input.txt") as file:
    sections = parsing.split_on_blank(file)
    monkeys = [Monkey(section) for section in sections]

inspections = [0] * len(monkeys)
for i in range(10000):
    for index in range(len(monkeys)):
        take_turn(index, 1)

sorted_inspections = sorted(enumerate(inspections), key=lambda p: p[1])
print(sorted_inspections)
print(sorted_inspections[-1][1] * sorted_inspections[-2][1])
