from __future__ import annotations

import random
from typing import Iterable

from logic_formula_generator.syntax_tree.first_order_logic import Predicate
from .functor_generator import FunctorGenerator
from .predicate_generator import PredicateGenerator
from .variable_generator import VariableGenerator


class PredicateSafetyLivenessGenerator(PredicateGenerator):
    def __init__(self, variable_gen: VariableGenerator, arities: Iterable[int], predicate_names: Iterable[str],
                 functor_gen: FunctorGenerator, safety_liveness_ratio: float = 0.5):
        """safety_liveness_ratio range [0, 1] - 0 means all predicates represent safety"""
        super().__init__(variable_gen, arities, predicate_names, functor_gen)
        self.safety_liveness_ratio = safety_liveness_ratio

    def generate(self) -> Predicate:
        # decide if predicate will present safety or liveness
        if random.random() > self.safety_liveness_ratio:
            return self.generate_predicate_with_variables()
        else:
            return self.generate_predicate_with_functors()

    def generate_predicate_with_functors(self) -> Predicate:
        """liveness property"""
        arity = random.choice(self.arities)
        p = Predicate(name=random.choice(self.predicate_name_for_arity[arity]), children=[])
        for i in range(arity):
            p.append(self.functor_gen.generate())
        return p

    def generate_predicate_with_variables(self) -> Predicate:
        """safety property (if variables are universally quantified)"""
        arity = random.choice(self.arities)
        p = Predicate(name=random.choice(self.predicate_name_for_arity[arity]), children=[])
        for i in range(arity):
            p.append(self.variable_gen.generate())
        return p
