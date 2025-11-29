from collections import defaultdict
from typing import Callable, TypeVar

_K = TypeVar("_K")
_V = TypeVar("_V")
class KeyedDefaultdict[_K, _V](defaultdict[_K, _V]):
    def __init__(self, kdf:Callable[[_K], _V], /, **kwargs):
        super().__init__(None, **kwargs)
        self.keyed_default_factory = kdf

    def __missing__(self, key):
        if self.keyed_default_factory:
            dict.__setitem__(self, key, self.keyed_default_factory(key))
            return self[key]
        else:
            return defaultdict.__missing__(self, key)
