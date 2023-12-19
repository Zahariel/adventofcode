import operator
from collections import defaultdict
from functools import reduce

import portion as P
from parsy import alt, char_from, regex, seq, string

from parsing import number, split_on_blank

def parse_workflow(line):
    name = regex(r"[a-z]{2,3}")
    target = alt(name, char_from("AR"))
    rule = seq(
        char_from("xmas"),
        char_from("<>"),
        number,
        string(":") >> target,
    ).map(tuple)

    parser = seq(
        name << string("{"),
        rule.sep_by(string(",")),
        string(",") >> target << string("}")
    )
    return parser.parse(line)

def parse_part(line):
    value = seq(
        char_from("xmas"),
        string("=") >> number
    )
    parser = string("{") >> value.sep_by(string(","), min=4, max=4).map(dict) << string("}")
    return parser.parse(line)

OPS = {
    '<': operator.lt,
    '>=': operator.ge,
}

class Workflow:
    def __init__(self, rules, final):
        self.rules = [(v, op, t, next) if op == '<' else (v, '>=', t+1, next) for (v, op, t, next) in rules]
        self.final = final

    def process_part(self, part):
        for value, op, threshold, target in self.rules:
            if OPS[op](part[value], threshold):
                return target
        return self.final

    def refine_proto(self, proto:dict[str, P.Interval]):
        result:dict[str, list[dict[str, P.Interval]]] = defaultdict(list)
        for value, op, threshold, target in self.rules:
            lo, hi = dict(proto), dict(proto)
            lo[value] &= P.closedopen(-P.inf, threshold)
            hi[value] -= P.closedopen(-P.inf, threshold)
            if op == '<':
                result[target].append(lo)
                proto = hi
            else:
                proto = lo
                result[target].append(hi)

        result[self.final].append(proto)

        # remove any refinement of 0 size
        return {next: [proto for proto in protos if proto_size(proto) > 0] for (next, protos) in result.items()}

    def __repr__(self):
        return f"Workflow({self.rules}, '{self.final}')"

with open("input.txt") as file:
    workflows, parts = split_on_blank(file)

    workflows = [parse_workflow(workflow.strip()) for workflow in workflows]
    workflows = {name: Workflow(rules, final) for (name, rules, final) in workflows}

    parts = [parse_part(line.rstrip()) for line in parts]


def eval_part(part):
    current = 'in'
    while current not in {'A', 'R'}:
        workflow = workflows[current]
        current = workflow.process_part(part)

    return current

print(sum(sum(part.values()) for part in parts if eval_part(part) == 'A'))



MIN = 1
MAX = 4001
initial_proto = {stat: P.closedopen(MIN, MAX) for stat in "xmas"}
needs_refinement = {
    'in': [initial_proto]
}

def proto_size(proto):
    # all of the portions should be atomic anyway, but i might as well do it properly
    return reduce(operator.mul, (sum(atom.upper - atom.lower for atom in p) for p in proto.values()))


accepted = []
while len(needs_refinement) > 0:
    next_run = defaultdict(list)
    for key, protos in needs_refinement.items():
        workflow = workflows[key]
        for proto in protos:
            for new_key, new_protos in workflow.refine_proto(proto).items():
                if new_key == 'A':
                    accepted.extend(new_protos)
                elif new_key == 'R':
                    # don't care about rejected
                    pass
                else:
                    next_run[new_key].extend(new_protos)
    needs_refinement = next_run

print(sum(proto_size(proto) for proto in accepted))

