

def choose_list(sets):
    decisions_dict = choose_dict(dict(enumerate(sets)))
    return [decisions_dict[i] for i in range(len(decisions_dict))]

def choose_dict(sets):
    decisions = {key: None for key in sets}
    possibilities = {key: set(val) for key, val in sets.items()}
    while any(val is None for val in decisions.values()):
        # find something with 1 possibility
        idx, s = next(filter(lambda p: len(p[1]) == 1, possibilities.items()))
        val = s.pop()
        decisions[idx] = val
        # take that possibility out of everything
        [poss.discard(val) for poss in possibilities.values()]
    return decisions
