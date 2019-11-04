import collections
import types
from random import randint
from typing import Iterable


def random_chain(*args) -> Iterable:
    args = list(args)
    while args:
        index = randint(0, len(args) - 1)
        if isinstance(args[index], types.GeneratorType):
            try:
                yield next(args[index])
            except StopIteration:
                del args[index]
        elif isinstance(args[index], list):
            try:
                yield args[index].pop()
            except IndexError:
                del args[index]
        elif isinstance(args[index], collections.abc.Iterable):
            raise NotImplementedError
        else:
            yield args[index]
            del args[index]
