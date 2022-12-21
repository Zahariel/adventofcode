import operator
import re

class Monkey:
    def __init__(self, name):
        self.name = name
        self.has_humn = (self.name == 'humn')

    def evaluate(self, monkeys):
        raise NotImplemented

    def solve(self, target, monkeys):
        raise NotImplemented

class NumMonkey(Monkey):
    def __init__(self, name, number):
        super().__init__(name)
        self.number = number

    def evaluate(self, monkeys):
        return self.number, self.has_humn

    def __repr__(self):
        return f"NumMonkey({self.name}, {self.number})"

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
}

# to solve left side: (target, right) -> answer
LEFT_REV_OPS = {
    '+': operator.sub,
    '-': operator.add,
    '*': operator.floordiv,
    '/': operator.mul,
}

# to solve right side: (target, left) -> answer
RIGHT_REV_OPS = {
    '+': operator.sub,
    '-': lambda t, l: l - t,
    '*': operator.floordiv,
    '/': lambda t, l: l // t,
}

class OpMonkey(Monkey):
    def __init__(self, name, first, op, second):
        super().__init__(name)
        self.second = second
        self.op = op
        self.first = first
        self.result = None
        self.has_humn = False

    def evaluate(self, monkeys):
        if self.result is None:
            left, left_humn = monkeys[self.first].evaluate(monkeys)
            right, right_humn = monkeys[self.second].evaluate(monkeys)
            self.result = OPS[self.op](left, right)
            self.has_humn = left_humn or right_humn
        return self.result, self.has_humn

    def solve(self, target, monkeys):
        if monkeys[self.first].has_humn:
            right, _ = monkeys[self.second].evaluate(monkeys)
            left_needed = LEFT_REV_OPS[self.op](target, right)
            return monkeys[self.first].solve(left_needed, monkeys)
        else:
            left, _ = monkeys[self.first].evaluate(monkeys)
            right_needed = RIGHT_REV_OPS[self.op](target, left)
            return monkeys[self.second].solve(right_needed, monkeys)

    def __repr__(self):
        return f"OpMonkey({self.name}, {self.first}, {self.op}, {self.second}, {self.result})"

def parse(line):
    result = re.match(r"([a-z]+): (\d+)", line)
    if result is not None:
        [name, value] = result.groups()
        return NumMonkey(name, int(value))
    else:
        [name, first, op, second] = re.match(r"([a-z]+): ([a-z]+) (.) ([a-z]+)", line).groups()
        return OpMonkey(name, first, op, second)

with open("input.txt") as file:
    raw_monkeys = [parse(line.rstrip()) for line in file]

# print(raw_monkeys)
monkeys = {monkey.name: monkey for monkey in raw_monkeys}

result = monkeys['root'].evaluate(monkeys)
print(result)

# part 2

class Human(Monkey):
    def __init__(self, name):
        super().__init__(name)

    def evaluate(self, monkeys):
        raise self

    def solve(self, target, monkeys):
        return target

    def __repr__(self):
        return f"Human({self.name})"

monkeys['humn'] = Human('humn')

left = monkeys[monkeys['root'].first]
right = monkeys[monkeys['root'].second]

if left.has_humn:
    humn = left.solve(right.evaluate(monkeys)[0], monkeys)
else:
    humn = right.solve(left.evaluate(monkeys)[0], monkeys)

print(humn)
