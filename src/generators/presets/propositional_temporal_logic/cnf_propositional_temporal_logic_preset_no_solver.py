from __future__ import annotations

from typing import Iterable

import src.generators.syntax_tree_generators.propositional_temporal_logic as ptl_gen
import src.generators.syntax_tree_generators.propositional_temporal_logic.normal_forms as ptl_normal_form_gen
import src.syntax_tree.propositional_temporal_logic as ptl
from src.generators import SyntaxTreeGenerator
from src.syntax_tree import TemporalLogicConnective


class CNFPropositionalTemporalLogicPresetNoSolver(SyntaxTreeGenerator):
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
        cnf_form_gen = ptl_normal_form_gen.CNFFormulaGenerator(
            var_gen=var_gen,
            negation_probability=self.negation_probability,
            unary_connectives=self.unary_connective, unary_connectives_weights=self.unary_connective_weights,
            clause_lengths=self.clause_lengths, clause_lengths_weights=self.clause_lengths_weights,
            min_number_of_clauses=self.min_number_of_clauses, min_number_of_variables=self.min_number_of_variables
        )
        return cnf_form_gen.generate()
