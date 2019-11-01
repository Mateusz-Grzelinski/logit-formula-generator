from __future__ import annotations

import collections
import types
from itertools import combinations_with_replacement
from random import sample, randint
from typing import Generator, Iterable

from src.ast import _connectives
from src.ast.first_order_logic import Atom, Variable
from src.generators import AstGenerator

variable = Variable('V')


def random_chain(*args):
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


class AtomSignatureGenerator(AstGenerator):
    def __init__(self, allowed_connectives: Iterable[str], predicate_gen: PredicateGenerator):
        self.predicate_gen = predicate_gen
        self.allowed_connective_properties = set(_connectives.get_connective_properties(connective) for connective in
                                                 allowed_connectives)

    def generate(self, random: bool = True) -> Generator[Atom, None, None]:
        global variable
        random_connectives = sample(self.allowed_connective_properties, len(self.allowed_connective_properties))
        connective_properties = random_connectives if random else self.allowed_connective_properties

        def atom_with_defined_connective(connective: ConnectiveProperties):
            for items in combinations_with_replacement(random_chain(self.predicate_gen.generate(), [variable]),
                                                       connective.arity):
                yield Atom(items=items, connective=connective.connective)

        generators = []
        for connective in connective_properties:
            generators.append(atom_with_defined_connective(connective=connective))

        while generators:
            index = randint(0, len(generators) - 1)
            try:
                yield next(generators[index])
            except StopIteration:
                del generators[index]