from __future__ import annotations

import random
from typing import Sequence

from src.generators import SyntaxTreeGenerator
from src.generators.syntax_tree_generators.first_order_logic import AtomGenerator
from src.syntax_tree import LogicalConnective
from src.syntax_tree.first_order_logic import FirstOrderLogicFormula


class CNFFormulaGenerator(SyntaxTreeGenerator):
    def __init__(self, atom_gen: AtomGenerator, clause_lengths: Sequence[int], clause_lengths_weights: Sequence[float],
                 min_number_of_clauses: int, min_number_of_literals: int, negation_probability: float):
        self.atom_gen = atom_gen
        self.clause_lengths_weights = clause_lengths_weights
        self.clause_lengths = clause_lengths
        self.negation_probability = negation_probability
        self.min_number_of_literals = min_number_of_literals
        self.min_number_of_clauses = min_number_of_clauses

    def generate(self) -> FirstOrderLogicFormula:
        root = FirstOrderLogicFormula(children=[], binary_logical_connective=LogicalConnective.AND)
        number_of_clauses = 0
        number_of_atoms = 0  # or number_of_literals - it is the same
        while True:
            clause_length = random.choices(population=self.clause_lengths, weights=self.clause_lengths_weights)[0]
            clause = FirstOrderLogicFormula(children=[], binary_logical_connective=LogicalConnective.OR)
            for _ in range(clause_length):
                atom = self.atom_gen.generate()
                if random.random() < self.negation_probability:
                    atom.unary_connectives.append(LogicalConnective.NOT)
                clause.append(atom)
                number_of_atoms += 1
            root.append(clause)
            number_of_clauses += 1
            if number_of_clauses > self.min_number_of_clauses and number_of_atoms > self.min_number_of_literals:
                return root
