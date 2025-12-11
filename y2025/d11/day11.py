import operator
from collections import Counter
from functools import reduce
from typing import NamedTuple, Iterable

from parsy import seq, string, regex, whitespace

from dag import Dag


class Device(NamedTuple):
    name: str
    outputs: list[str]

def parse(line) -> Device:
    name = regex(r"...")
    device = seq(name << string(":") << whitespace, name.sep_by(whitespace)).combine(Device)
    return device.parse(line)


with open("input.txt") as f:
    devices = dict([parse(line.rstrip()) for line in f])

dag = Dag.from_children(devices)

results = dag.propagate_values({"you": 1}, sum)

print(results["out"])


def combiner(node, vals:Iterable[Counter[frozenset]]):
    result: Counter[frozenset] = reduce(operator.add, vals, Counter())
    if node in {"dac", "fft"}:
        result = Counter({frozenset(flags | {node}): count for flags, count in result.items()})
    return result


results_2 = dag.propagate_named_values({"svr": Counter({frozenset(): 1})}, combiner)

print(results_2["out"][frozenset({"dac", "fft"})])
