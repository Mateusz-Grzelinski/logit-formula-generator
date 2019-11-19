import collections
import random
import types
from copy import copy
from itertools import *
from typing import Generator, Any, NewType, Iterable

Item = NewType('Item', Any)


# combinations_with_replacement()  # order does not matter
# permutations()  # order matters
# product()  # same as combinations

# https://stackoverflow.com/questions/12093364/cartesian-product-of-large-iterators-itertools/12094519#12094519
# def lazy_product(*args: Generator):
#     if not args:
#         yield []
#         return
#
#     for i in args[0]:
#         args_copy = []
#         for gen_original, gen_copy in args[1:]:
#             args_copy.append(gen_copy)
#         for js in lazy_product(*args_copy):
#             yield [i] + js

def iterProduct(ic):
    if not ic:
        yield []
        return
    for i in ic[0]():
        for js in iterProduct(ic[1:]):
            yield [i] + js


def lazy_product(*args: Generator):
    assert all(args[i] is not args[len(args) - i - 1] for i in range(len(args) // 2) if
               isinstance(args[i], types.GeneratorType)), 'generator must be unique'

    def _lazy_product_helper(*args: Generator):
        if not args:
            yield []
            return

        for i in copy(args[0]):
            for js in lazy_product(*args[1:]):
                yield [i] + js

    # generators does not support copy, but tee does
    args_copy = [tee(i)[1] for i in args]
    return _lazy_product_helper(*args_copy)


def lazy_combinations_with_replacement(gen: Generator, r: int):
    if r == 0:
        yield []
        return

    _gen_master, gen_copy1, gen_copy2 = tee(gen, 3)
    for i in gen_copy1:
        for js in lazy_combinations_with_replacement(gen_copy2, r - 1):
            yield [i] + js


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


def random_lazy_product(*args: Generator):
    assert all(args[i] is not args[len(args) - i - 1] for i in range(len(args) // 2) if
               isinstance(args[i], types.GeneratorType)), 'generator must be unique'
    skip_chance = random.random()

    def _random_lazy_product_helper(*args: Generator):
        nonlocal skip_chance
        if not args:
            yield []
            return
        cache = []
        generators = []
        for i in copy(args[0]):
            cache.append(i)
            generators.append(_random_lazy_product_helper(*args[1:]))
            if random.random() > skip_chance:
                continue
            else:
                random_index = random.randrange(len(generators))
                try:
                    js = next(generators[random_index])
                    yield [i] + js
                except StopIteration:
                    del generators[random_index]

        while generators:
            random_index = random.randrange(len(generators))
            try:
                js = next(generators[random_index])
                yield [cache[random_index]] + js
            except StopIteration:
                del generators[random_index]
                del cache[random_index]

    # generators does not support copy, but tee does
    args_copy = [tee(i)[1] for i in args]
    return _random_lazy_product_helper(*args_copy)


if __name__ == '__main__':
    a_gen = (i for i in range(5))
    b_gen = (i for i in ['a', 'b'])
    c_gen = (i for i in ['c', 'd'])
    a = lambda: (i for i in [0, 1, 2])
    b = lambda: (i for i in ['a', 'b'])
    c = lambda: (i for i in ['c', 'd'])

    # for i in enumerate(lazy_combinations_with_replacement(a_gen, 3)):
    #     print(i)

    # same as:
    # for i in enumerate(product([0, 1], [0, 1], [0, 1])):
    #     print(i)

    # print('lazy product combinations')
    # comb = []
    # comb.append(lazy_combinations_with_replacement(a_gen, 20))
    # comb.append(lazy_combinations_with_replacement(b_gen, 3))
    # for i in enumerate(lazy_product(*comb)):
    #     print(i)

    print('lazy product:')
    for i in enumerate(random_lazy_product(a_gen, b_gen)):
        print(i)

    # for i in enumerate(iterProduct([
    #     # lambda: lazy_combinations(b_gen, 3)
    #     lambda: (i for i in [0, 1, 2]),
    #     lambda: lazy_combinations(a_gen, 2),
    #     # lambda: (i for i in [3, 4, 5])
    # ])):
    #     pass
    #     print(i)
# print(_n_item(a, 2))
# for i in lazy_product(a, b, c):
#     print(i)
