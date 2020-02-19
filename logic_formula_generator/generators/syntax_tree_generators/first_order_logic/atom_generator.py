from __future__ import annotations

import random
from typing import Iterable, Union

from logic_formula_generator.generators import SyntaxTreeGenerator
from logic_formula_generator.syntax_tree import get_connective_properties, LogicalConnective
from logic_formula_generator.syntax_tree.first_order_logic import Atom


class AtomGenerator(SyntaxTreeGenerator):
    def __init__(self, math_connectives: Iterable[Union[str, None]], negation_chance: float,
                 variable_gen: VariableGenerator = None, predicate_gen: PredicateGenerator = None,
                 functor_gen: FunctorGenerator = None):
        self.negation_chance = negation_chance
        self.functor_gen = functor_gen
        self.variable_name_gen = variable_gen
        self.predicate_gen = predicate_gen

        self.allowed_math_connectives = list(math_connectives)
        for i, connective in enumerate(self.allowed_math_connectives):
            if connective is not None:
                self.allowed_math_connectives[i] = get_connective_properties(connective)

    def generate(self) -> Atom:
        math_connective = random.choice(self.allowed_math_connectives)
        unary_connective = [LogicalConnective.NOT] if random.random() < self.negation_chance else []
        if math_connective is None:
            return Atom(children=[self.predicate_gen.generate()], math_connective=None,
                        unary_connective=unary_connective)
        if math_connective.arity == 1:
            return Atom(children=[self.predicate_gen.generate()], math_connective=math_connective,
                        unary_connective=unary_connective)
        elif math_connective.arity == 2:
            a = Atom(children=[], math_connective=math_connective, unary_connective=unary_connective)
            for i in range(math_connective.arity):
                if random.randint(0, 1):
                    a.append(self.functor_gen.generate())
                else:
                    a.append(self.variable_name_gen.generate())
            return a
