import operator
from functools import reduce
from itertools import combinations

from parsy import seq, string, whitespace
import z3

from breadth_first import a_star
from parsing import number


class Machine:
    def __init__(self, indicators, buttons, joltage):
        self.indicators = indicators
        self.buttons = buttons
        self.joltage = joltage
        self.biggest_button = max(len(button) for button in buttons)

    def __repr__(self):
        return f"Machine({self.indicators}, {self.buttons}, {self.joltage})"

    def least_presses(self):
        for i in range(1, len(self.buttons) + 1):
            for combo in combinations(self.buttons, i):
                result = reduce(operator.xor, combo)
                if result == self.indicators:
                    return i
        raise ValueError

    # this "works" but it is WAY too slow
    def fix_joltage(self):
        print(f"attempting machine {self}")
        target_sum = sum(self.joltage)

        # i have to multiply all costs by biggest_button here so that the estimator is admissible without division
        def neighbors(state):
            levels, total = state
            for button in self.buttons:
                new_levels = tuple([level + 1 if i in button else level for i, level in enumerate(levels)])
                if all(reached <= target for reached, target in zip(new_levels, self.joltage)):
                    yield self.biggest_button, (new_levels, total + len(button))

        def process(_, dist, state):
            levels, _ = state
            if levels == self.joltage:
                return dist
            return None

        # maybe i could do a better estimator here, this is just manhattan distance. euclidean distance?
        # but it would be SO SLOW to calculate. but i don't think it really matters, the problem is the whole idea
        # i tried it with euclidean distance, it didn't make a difference
        def estimator(state):
            return target_sum - state[1]

        start = tuple([0 for _ in self.joltage])
        presses = a_star([(start, 0)], neighbors_fn=neighbors, process_fn=process, estimator_fn=estimator)
        assert presses
        return presses // self.biggest_button

    # this is cheating because it uses z3, but it's FAST
    def fix_joltage_z3(self):
        s = z3.Optimize()
        counts = [z3.Int(f"button_{k}") for k in range(len(self.buttons))]
        s.add(*(count >= 0 for count in counts))

        for i, jolt in enumerate(self.joltage):
            s.add(z3.Sum(*(count for button, count in zip(self.buttons, counts) if i in button)) == jolt)

        h = s.minimize(z3.Sum(*counts))
        assert s.check() == z3.sat
        return h.lower().as_long()


def parse(line):
    indicator = string(".") | string("#")
    indicators = string("[") >> indicator.many().map(
        lambda things: {idx for idx, ind in enumerate(things) if ind == "#"},
    ) << string("]")

    button = string("(") >> number.sep_by(string(",")).map(set) << string(")")
    buttons = button.sep_by(whitespace)

    joltage = string("{") >> number.sep_by(string(",")).map(tuple) << string("}")

    machine = seq(indicators, whitespace >> buttons, whitespace >> joltage).combine(Machine)

    return machine.parse(line)


with open("input.txt") as f:
    lines = [parse(line.rstrip()) for line in f]

print(sum(machine.least_presses() for machine in lines))

print(sum(machine.fix_joltage_z3() for machine in lines))
