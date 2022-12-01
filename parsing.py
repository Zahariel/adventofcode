import typing

T = typing.TypeVar('T')

def split_on_blank(lines:typing.Iterable[str], line_parser:typing.Optional[typing.Callable[[str],T]]=None) -> typing.Generator[typing.List[T], None, None]:
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

