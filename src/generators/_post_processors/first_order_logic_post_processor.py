from __future__ import annotations

import random
from typing import Iterable

import src.ast.first_order_logic as fol
from ._post_processor import PostProcessor


class FOLPostProcessor(PostProcessor):
    def __init__(self, predicate_names: Iterable[str], functor_names: Iterable[str], variable_names: Iterable[str]):
        self.variable_names = set(variable_names)
        self.predicate_names = set(predicate_names)
        self.functor_names = set(functor_names)

    def post_process(self, formula: fol.CNFFormula):
        # self.switch_names(formula)
        self.apply_random_sign(formula)

    # def switch_names(self, formula: fol.CNFFormula):
    #     for predicate in formula.items(type=fol.Predicate):
    #         predicate.name = random.sample(self.predicate_names, 1)[0]
    #     for functor in formula.items(type=fol.Functor):
    #         functor.name = random.sample(self.functor_names, 1)[0]
    #     for variable in formula.items(type=fol.Variable):
    #         variable.name = random.sample(self.variable_names, 1)[0]
    #
    def apply_random_sign(self, formula: fol.CNFFormula):
        from src.ast.first_order_logic import Literal
        for literal in formula.items(type=Literal):
            literal.is_negated = bool(random.randint(0, 1))
