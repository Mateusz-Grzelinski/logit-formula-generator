from __future__ import annotations

from itertools import combinations_with_replacement, chain
from random import sample, randint
from typing import Generator, Iterable

from src.ast import connectives
from src.ast.first_order_logic import Atom, Variable

variable = Variable('V')


class AtomSignatureGenerator:
    def __init__(self, allowed_connectives: Iterable[str], predicate_gen: PredicateGenerator):
        self.predicate_gen = predicate_gen
        self.allowed_connective_properties = set(connectives.get_operand_properties(connective) for connective in
                                                 allowed_connectives)

    def generate(self, random: bool = True) -> Generator[Atom, None, None]:
        global variable
        random_connectives = sample(self.allowed_connective_properties, len(self.allowed_connective_properties))
        connective_properties = random_connectives if random else self.allowed_connective_properties

        def atom_with_defined_connective(connective: ConnectiveProperties):
            for items in combinations_with_replacement(chain(self.predicate_gen.generate(), [variable]),
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
