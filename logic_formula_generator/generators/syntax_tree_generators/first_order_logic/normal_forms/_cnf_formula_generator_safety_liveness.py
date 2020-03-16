from __future__ import annotations

import random
from typing import Sequence

from logic_formula_generator.generators import SyntaxTreeGenerator
from logic_formula_generator.generators.syntax_tree_generators.first_order_logic import AtomGenerator
from logic_formula_generator.generators.syntax_tree_generators.first_order_logic.atom_safety_liveness_generator import \
    AtomSafetyLivenessGenerator
from logic_formula_generator.generators.syntax_tree_generators.first_order_logic.normal_forms import CNFFormulaGenerator
from logic_formula_generator.syntax_tree import LogicalConnective
from logic_formula_generator.syntax_tree.first_order_logic import FirstOrderLogicFormula


class CNFFormulaGeneratorSafetyLiveness(CNFFormulaGenerator):
    def __init__(self, atom_gen: AtomSafetyLivenessGenerator, clause_lengths: Sequence[int],
                 clause_lengths_weights: Sequence[float], min_number_of_clauses: int, min_number_of_literals: int,
                 negation_probability: float, safety_liveness_ratio: float):
        super().__init__(atom_gen, clause_lengths, clause_lengths_weights, min_number_of_clauses,
                         min_number_of_literals, negation_probability)
        self.safety_liveness_ratio = safety_liveness_ratio

    def generate(self) -> FirstOrderLogicFormula:
        root = FirstOrderLogicFormula(children=[], binary_logical_connective=LogicalConnective.AND)
        number_of_clauses = 0
        number_of_atoms = 0  # or number_of_literals - it is the same
        while True:
            clause_length = random.choices(population=self.clause_lengths, weights=self.clause_lengths_weights)[0]
            if random.random() > self.safety_liveness_ratio:
                clause = self.generate_safety_clause(clause_length)
            else:
                clause = self.generate_liveness_clause(clause_length)
            number_of_atoms += len(clause)
            root.append(clause)
            number_of_clauses += 1
            if number_of_clauses > self.min_number_of_clauses and number_of_atoms > self.min_number_of_literals:
                return root

    def generate_safety_clause(self, clause_length: int) -> FirstOrderLogicFormula:
        clause = FirstOrderLogicFormula(children=[], binary_logical_connective=LogicalConnective.OR)
        for _ in range(clause_length):
            atom = self.atom_gen.generate_with_variables()
            if random.random() < self.negation_probability:
                atom.unary_connectives.append(LogicalConnective.NOT)
            clause.append(atom)
        return clause

    def generate_liveness_clause(self, clause_length: int) -> FirstOrderLogicFormula:
        clause = FirstOrderLogicFormula(children=[], binary_logical_connective=LogicalConnective.OR)
        for _ in range(clause_length):
            atom = self.atom_gen.generate_with_functors()
            if random.random() < self.negation_probability:
                atom.unary_connectives.append(LogicalConnective.NOT)
            clause.append(atom)
        return clause
