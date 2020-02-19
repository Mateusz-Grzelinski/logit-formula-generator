from __future__ import annotations

import random
from typing import Iterable

from logic_formula_generator.generators import SyntaxTreeGenerator
from logic_formula_generator.syntax_tree.first_order_logic import Predicate
from .functor_generator import FunctorGenerator
from .variable_generator import VariableGenerator


class PredicateGenerator(SyntaxTreeGenerator):
    def __init__(self, variable_gen: VariableGenerator, arities: Iterable[int], predicate_names: Iterable[str],
                 functor_gen: FunctorGenerator):
        self.variable_gen = variable_gen
        self.arities = list(set(arities))
        self.functor_gen = functor_gen
        predicate_names = list(predicate_names)
        assert len(predicate_names) >= len(self.arities), \
            f'there must be at least {len(self.arities)} predicate names available'
        random.shuffle(predicate_names)
        self.predicate_name_for_arity = {}
        for arity in self.arities:
            self.predicate_name_for_arity[arity] = [predicate_names.pop()]
        while predicate_names:
            self.predicate_name_for_arity[random.choice(self.arities)].append(predicate_names.pop())

    def generate(self) -> Predicate:
        arity = random.choice(self.arities)
        p = Predicate(name=random.choice(self.predicate_name_for_arity[arity]), children=[])
        for i in range(arity):
            if random.randint(0, 1):
                p.append(self.variable_gen.generate())
            else:
                p.append(self.functor_gen.generate())
        return p
