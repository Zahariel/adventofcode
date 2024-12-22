from typing import TypeVar, Dict, Iterable

KEY = TypeVar("KEY")
VALUE = TypeVar("VALUE")


def find_and_replace_symbol(start: Dict[KEY, VALUE], symbol: VALUE, replacement: VALUE) -> KEY:
    for loc, cell in start.items():
        if cell == symbol:
            start[loc] = replacement
            return loc

def n_wise(coll: Iterable[VALUE], group_size:int) -> Iterable[tuple[VALUE, ...]]:
    """like itertools.pairwise() but can return tuples of any given size"""
    output = []
    for x in coll:
        output.append(x)
        if len(output) > group_size:
            output = output[1:]
        if len(output) == group_size:
            yield tuple(output)
