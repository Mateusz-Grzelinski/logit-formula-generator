from __future__ import annotations

import random
from typing import Sequence

import src.syntax_tree.propositional_temporal_logic as ptl
from src.generators import SyntaxTreeGenerator
from src.syntax_tree import ConnectiveProperties, LogicalConnective
from .._variable_generator import VariableGenerator


class CNFFormulaGenerator(SyntaxTreeGenerator):
    def __init__(self, var_gen: VariableGenerator,
                 negation_probability: float,
                 unary_connectives: Sequence[ConnectiveProperties], unary_connectives_weights: Sequence[float],
                 clause_lengths: Sequence[int], clause_lengths_weights: Sequence[float],
                 min_number_of_variables: int, min_number_of_clauses: int):
        self.var_gen = var_gen
        self.negation_probability = negation_probability
        self.unary_connective = unary_connectives
        self.unary_connective_weights = unary_connectives_weights
        self.clause_lengths = clause_lengths
        self.clause_lengths_weights = clause_lengths_weights
        self.min_number_of_variables = min_number_of_variables
        self.min_number_of_clauses = min_number_of_clauses

    def generate(self) -> ptl.PTLFormula:
        root = ptl.PTLFormula(children=[], logical_connective=LogicalConnective.AND)

        number_of_clauses = 0
        number_of_variables = 0
        while True:
            clause_length = random.choices(population=self.clause_lengths, weights=self.clause_lengths_weights)[0]
            clause = ptl.PTLFormula(children=[], logical_connective=LogicalConnective.OR)
            for _ in range(clause_length):
                variable = self.var_gen.generate()
                if unary_connective := random.choices(self.unary_connective, weights=self.unary_connective_weights)[0]:
                    variable.unary_connectives.append(unary_connective)
                if random.random() < self.negation_probability:
                    variable.unary_connectives.append(LogicalConnective.NOT)
                clause.append(variable)
                number_of_variables += 1
            root.append(clause)
            number_of_clauses += 1
            if number_of_clauses > self.min_number_of_clauses and number_of_variables > self.min_number_of_variables:
                return root
