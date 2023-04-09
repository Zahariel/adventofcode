from typing import TypeVar, Optional, Callable
from collections.abc import Iterable, Generator, Sequence

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

def chunks(things:Sequence[T], chunksize:int) -> Generator[Sequence[T], None, None]:
    for i in range(0, len(things), chunksize):
        yield things[i:i+chunksize]
