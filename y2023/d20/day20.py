import math
from collections import defaultdict, deque

from parsy import regex, seq, string, whitespace

class Module:
    def receive_signal(self, source, is_high):
        raise NotImplemented

    def add_input(self, input):
        pass

    def reset(self):
        pass

class FlipFlop(Module):
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
        self.status = False

    def __repr__(self):
        return f"%{self.name}[{self.status}] -> {self.outputs}"

    def receive_signal(self, source, is_high):
        if is_high:
            return True, []
        self.status = not self.status
        return self.status, self.outputs

    def reset(self):
        self.status = False

class Conjunction(Module):
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
        self.memory = dict()

    def __repr__(self):
        return f"&{self.name} [{self.memory}] -> {self.outputs}"

    def add_input(self, input):
        self.memory[input] = False

    def receive_signal(self, source, is_high):
        self.memory[source] = is_high
        return not all(self.memory.values()), self.outputs

    def reset(self):
        for k in self.memory:
            self.memory[k] = False

class Broadcaster(Module):
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs

    def receive_signal(self, source, is_high):
        return is_high, self.outputs

def make_device(name, outputs):
    if name == 'broadcaster':
        return Broadcaster(name, outputs)
    elif name[0] == '%':
        return FlipFlop(name[1:], outputs)
    elif name[0] == '&':
        return Conjunction(name[1:], outputs)


def parse(line):
    parser = seq(
        regex(r"[&%a-z]+") << whitespace,
        string("->") >> whitespace >> regex(r"[a-z]+").sep_by(string(", "))
    )
    return make_device(*parser.parse(line))



with open("input.txt") as file:
    lines = [parse(line.rstrip()) for line in file]
    modules = {module.name: module for module in lines}

for module in modules.values():
    for target in module.outputs:
        if target in modules:
            modules[target].add_input(module.name)



signals = defaultdict(int)
def press_button(watchlist):
    # print("press", i+1)
    outputs = set()
    message_bus = deque()
    message_bus.append(('button', 'broadcaster', False))
    while len(message_bus) > 0:
        source, actor, kind = message_bus.popleft()
        # print(source, actor, kind)
        signals[kind] += 1
        if actor in watchlist and not kind:
            outputs.add(actor)
        if actor not in modules:
            continue
        module = modules[actor]
        new_kind, targets = module.receive_signal(source, kind)
        message_bus.extend((actor, target, new_kind) for target in targets)
    return outputs

PRESSES = 1000
for i in range(PRESSES):
    press_button(set())

print(signals[False] * signals[True])


# part 2

# i calculated these by analyzing my input by hand
counters = [0b1111_0111_1111, 0b1111_1011_0101, 0b1111_0101_0011, 0b1111_0100_1101]
print(math.lcm(*counters))



# this is the simulation but it takes way, way, way too long

# for module in modules.values():
#     module.reset()
#
# seen = False
# presses = 0
# while not seen:
#     presses += 1
#     if presses % 1000 == 0:
#         print(presses)
#     outputs = press_button({'rx'})
#     if 'rx' in outputs:
#         seen = True
#
# print(presses)
