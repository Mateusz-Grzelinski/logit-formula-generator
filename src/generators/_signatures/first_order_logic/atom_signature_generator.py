from __future__ import annotations

from functools import partial
from itertools import combinations_with_replacement
from random import sample, randint
from typing import Generator, Iterable

from src.ast import ConnectiveProperties
from src.ast import get_connective_properties
from src.ast.first_order_logic import Atom, Variable
from src.generators import AstGenerator
from src.generators._random_chain import random_chain


class AtomSignatureGenerator(AstGenerator):
    variable_name = 'V'

    def __init__(self, allowed_connectives: Iterable[str], predicate_gen: PredicateSignatureGenerator,
                 random: bool = True):
        self.random = random
        self.predicate_gen = predicate_gen
        self.allowed_connective_properties = set(get_connective_properties(connective) for connective in
                                                 allowed_connectives)

    def generate(self) -> Generator[Atom, None, None]:
        def atom_with_defined_connective(connective: ConnectiveProperties) -> Generator[Atom, None, None]:
            for items in combinations_with_replacement(possible_arguments(), connective.arity):
                yield Atom(items=items, connective=connective.connective)

        random_connectives = sample(self.allowed_connective_properties, len(self.allowed_connective_properties))
        connective_properties = random_connectives if self.random else self.allowed_connective_properties
        possible_arguments = partial(random_chain, self.predicate_gen.generate(), Variable(name=self.variable_name))

        generators = []
        for connective in connective_properties:
            generators.append(atom_with_defined_connective(connective=connective))

        while generators:
            index = randint(0, len(generators) - 1)
            try:
                yield next(generators[index])
            except StopIteration:
                del generators[index]
