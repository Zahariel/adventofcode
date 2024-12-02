from collections.abc import Generator, Iterable, Sequence
from typing import Callable, Optional, TypeVar

import parsy

T = TypeVar('T')

def split_on_blank(lines:Iterable[str], line_parser: Optional[Callable[[str],T]]=None) -> Generator[list[T], None, None]:
    if line_parser is None:
        line_parser = lambda x:x
    group = []
    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            yield group
            group = []
        else:
            group.append(line_parser(line))
    yield group

# superseded by itertools.batched() in 3.12
def chunks(things:Sequence[T], chunksize:int) -> Generator[Sequence[T], None, None]:
    for i in range(0, len(things), chunksize):
        yield things[i:i+chunksize]


number = parsy.regex(r"-?\d+").map(int)
