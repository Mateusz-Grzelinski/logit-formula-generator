from __future__ import annotations

from itertools import combinations, combinations_with_replacement, chain
from typing import Generator, Set

from src.ast import operands
from src.ast.first_order_logic import Atom, Variable

variable = Variable('V')


class AtomSignatureGenerator:
    def __init__(self, allowed_connectives: Set[str], predicate_gen: PredicateGenerator):
        self.predicate_gen = predicate_gen
        self.allowed_connective_properties = set(operands.get_operand_properties(connective) for connective in
                                                 allowed_connectives)

    def generate(self) -> Generator[Atom, None, None]:
        global variable
        for connective in self.allowed_connective_properties:
            if connective.commutative:
                for items in combinations(chain(self.predicate_gen.generate(), [variable]), connective.arity):
                    yield Atom(items=items, connective=connective.connective)
            else:
                for items in combinations_with_replacement(chain(self.predicate_gen.generate(), [variable]),
                                                           connective.arity):
                    yield Atom(items=items, connective=connective.connective)
