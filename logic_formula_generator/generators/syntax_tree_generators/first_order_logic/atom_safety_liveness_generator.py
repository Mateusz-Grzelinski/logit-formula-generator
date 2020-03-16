from __future__ import annotations

import random
from typing import Iterable, Union

from logic_formula_generator.generators import SyntaxTreeGenerator
from logic_formula_generator.generators.syntax_tree_generators.first_order_logic.predicate_safety_liveness_generator import \
    PredicateSafetyLivenessGenerator
from logic_formula_generator.generators.syntax_tree_generators.first_order_logic.atom_generator import AtomGenerator
from logic_formula_generator.syntax_tree import get_connective_properties, LogicalConnective
from logic_formula_generator.syntax_tree.first_order_logic import Atom


class AtomSafetyLivenessGenerator(AtomGenerator):
    def __init__(self, predicate_gen: PredicateSafetyLivenessGenerator = None):
        self.predicate_gen: PredicateSafetyLivenessGenerator
        super().__init__(predicate_gen=predicate_gen)

    def generate(self) -> Atom:
        self.predicate_gen: PredicateSafetyLivenessGenerator
        return Atom(children=[self.predicate_gen.generate()], math_connective=None, unary_connective=[])

    def generate_with_variables(self) -> Atom:
        self.predicate_gen: PredicateSafetyLivenessGenerator
        return Atom(children=[self.predicate_gen.generate_predicate_with_variables()], math_connective=None,
                    unary_connective=[])

    def generate_with_functors(self) -> Atom:
        self.predicate_gen: PredicateSafetyLivenessGenerator
        return Atom(children=[self.predicate_gen.generate_predicate_with_functors()], math_connective=None,
                    unary_connective=[])
