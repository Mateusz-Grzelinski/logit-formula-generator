from __future__ import annotations

from random import sample, randint
from typing import Generator, Iterable

from src.ast import ConnectiveProperties
from src.ast import get_connective_properties
from src.ast.first_order_logic import Atom, Variable
from src.generators import AstGenerator
from src.generators.utils._ensure_unique_id import ensure_unique_id
from src.generators.utils._lazy_itertools import random_chain, random_lazy_combinations_with_replacement


class AtomSignatureGenerator(AstGenerator):
    variable_name = 'V'

    def __init__(self, connectives: Iterable[str], predicate_gen: PredicateSignatureGenerator,
                 random: bool = True):
        self.random = random
        self.predicate_gen = predicate_gen
        self.allowed_connective_properties = set(get_connective_properties(connective) for connective in
                                                 connectives)

    def generate(self) -> Generator[Atom, None, None]:
        def atom_with_defined_connective(connective: ConnectiveProperties) -> Generator[Atom, None, None]:
            possible_arguments = random_chain(self.predicate_gen.generate(), Variable(name=self.variable_name))
            for items in random_lazy_combinations_with_replacement(possible_arguments, connective.arity):
                yield Atom(items=ensure_unique_id(items), connective=connective.connective)

        random_connectives = sample(self.allowed_connective_properties, len(self.allowed_connective_properties))
        connective_properties = random_connectives if self.random else self.allowed_connective_properties

        generators = []
        for connective in connective_properties:
            generators.append(atom_with_defined_connective(connective=connective))

        while generators:
            index = randint(0, len(generators) - 1)
            try:
                yield next(generators[index])
            except StopIteration:
                del generators[index]
