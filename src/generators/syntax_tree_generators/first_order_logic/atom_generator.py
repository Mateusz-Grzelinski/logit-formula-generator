from __future__ import annotations

import random
from typing import Iterable

from src.ast import get_connective_properties
from src.ast.first_order_logic import Atom
from src.generators import AstGenerator


class AtomGenerator(AstGenerator):
    # variable_name = 'V'

    def __init__(self, variable_gen: VariableGenerator, connectives: Iterable[str],
                 predicate_gen: PredicateGenerator):
        self.variable_name_gen = variable_gen
        self.predicate_gen = predicate_gen
        self.allowed_connectives = list(get_connective_properties(connective) for connective in connectives)

    def generate(self) -> Atom:
        connective = random.choice(self.allowed_connectives)
        if connective.arity == 1:
            return Atom(items=[self.predicate_gen.generate()], connective=connective)
        elif connective.arity == 2:
            a = Atom(items=[], connective=connective)
            for i in range(connective.arity):
                if random.randint(0, 1):
                    a.append(self.predicate_gen.generate())
                else:
                    a.append(self.variable_name_gen.generate())
            return a
