from __future__ import annotations

import random
from typing import Iterable

from src.ast.first_order_logic import CNFFormula


class FOLPostProcessor:
    def __init__(self, predicate_names: Iterable[str], functor_names: Iterable[str], variable_names: Iterable[str]):
        self.variable_names = variable_names
        self.predicate_names = predicate_names
        self.functor_names = functor_names

    def switch_names(self, formula: CNFFormula):
        from src.ast.first_order_logic import Variable, Functor, Predicate, Literal
        for literal in formula.items(type=Literal):
            literal.is_negated = bool(random.randint(0, 1))
        for predicate in formula.items(type=Predicate):
            predicate.name = random.sample(self.predicate_names, 1)[0]
        for functor in formula.items(type=Functor):
            functor.name = random.sample(self.functor_names, 1)[0]
        for variable in formula.items(type=Variable):
            variable.name = random.sample(self.variable_names, 1)[0]
