import collections
import random
import types
from typing import Generator, Any, NewType, Iterable, List

# _cache: weakref.

Item = NewType('Item', Any)


def _lazy_product(*args: Generator[Item, Any, Any], tmp=None):
    # algorithm is called recursive descent
    tmp = tmp if tmp else []
    if not args:
        yield tmp
    else:
        for i in args[0]:
            yield from _lazy_product(*args[1:], tmp=tmp + [i])


def lazy_product(*args: Generator[Item, Any, Any]) -> Generator[List[Item], Any, None]:
    return _lazy_product(*args, tmp=None)


def random_chain(*args) -> Iterable:
    args = list(args)
    while args:
        index = random.randint(0, len(args) - 1)
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


if __name__ == '__main__':
    a = (i for i in [0, 1, 2])
    b = (i for i in ['a', 'b'])
    c = (i for i in ['c', 'd'])
    # print(_n_item(a, 2))
    for i in lazy_product(a, b, c):
        print(i)
