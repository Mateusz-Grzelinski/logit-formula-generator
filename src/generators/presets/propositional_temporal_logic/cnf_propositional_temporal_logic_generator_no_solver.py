from __future__ import annotations

import random
from typing import Iterable

import src.generators.syntax_tree_generators.propositional_temporal_logic as ptl_gen
import src.syntax_tree.propositional_temporal_logic as ptl
from src.generators import SyntaxTreeGenerator
from src.syntax_tree import LogicalConnective, TemporalLogicConnective


class CNFPropositionalTemporalLogicGeneratorNoSolver(SyntaxTreeGenerator):
    """Currently used only in examples/temporal_logic/thesis/k_sat.py"""

    def __init__(self, variable_names: Iterable[str],
                 variable_without_connective_probability: float,
                 variable_with_always_connective_probability: float,
                 variable_with_eventually_connective_probability: float,
                 clause_lengths: Iterable[int],
                 min_number_of_clauses: int,
                 min_number_of_variables: int,
                 clause_lengths_weights: Iterable[float],
                 variable_negation_probability=0.1) -> None:
        self.unary_connective = [
            None,
            TemporalLogicConnective.ALWAYS,
            TemporalLogicConnective.EVENTUALLY
        ]
        self.unary_connective_weights = [
            variable_without_connective_probability,
            variable_with_always_connective_probability,
            variable_with_eventually_connective_probability
        ]
        self.min_number_of_clauses = min_number_of_clauses
        self.min_number_of_variables = min_number_of_variables
        self.clause_lengths = list(clause_lengths)
        self.clause_lengths_weights = list(clause_lengths_weights)
        self.negation_probability = variable_negation_probability
        self.variable_names = set(variable_names)

    def generate(self) -> ptl.PTLFormula:
        var_gen = ptl_gen.VariableGenerator(variable_names=self.variable_names)
        root = ptl.PTLFormula(children=[], logical_connective=LogicalConnective.AND)

        number_of_clauses = 0
        number_of_variables = 0
        while True:
            clause_length = random.choices(population=self.clause_lengths, weights=self.clause_lengths_weights)[0]
            clause = ptl.PTLFormula(children=[], logical_connective=LogicalConnective.OR)
            for _ in range(clause_length):
                variable = var_gen.generate()
                if random.random() < self.negation_probability:
                    variable.unary_connectives.append(LogicalConnective.NOT)
                if unary_connective := random.choices(self.unary_connective, weights=self.unary_connective_weights)[0]:
                    variable.unary_connectives.append(unary_connective)
                clause.append(variable)
                number_of_variables += 1
            root.append(clause)
            number_of_clauses += 1
            if number_of_clauses > self.min_number_of_clauses and number_of_variables > self.min_number_of_variables:
                return root
