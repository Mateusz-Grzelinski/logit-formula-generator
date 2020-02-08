from __future__ import annotations

import random
from typing import Iterable

import src.generators.syntax_tree_generators.propositional_temporal_logic as ptl_gen
import src.syntax_tree.propositional_temporal_logic as ptl
from src.generators import SyntaxTreeGenerator, IntegerRange
from src.generators.contraint_solver.first_order_logic.z3_solver import Z3CNFConstraintSolver
from src.syntax_tree import LogicalConnective, TemporalLogicConnective


class CNFPropositionalTemporalLogicGenerator(SyntaxTreeGenerator):
    def __init__(self, variable_names: Iterable[str], number_of_variables_without_connective: IntegerRange,
                 number_of_variables_with_always_connectives: IntegerRange,
                 number_of_variables_with_eventually_connectives: IntegerRange, number_of_clauses: IntegerRange,
                 clause_lengths: Iterable[int], negation_probability=0.1) -> None:
        self.number_of_variables_without_connective = number_of_variables_without_connective
        self.number_of_variables_with_always_connectives = number_of_variables_with_always_connectives
        self.number_of_variables_with_eventually_connectives = number_of_variables_with_eventually_connectives
        self.number_of_clauses = number_of_clauses
        self.clause_lengths = set(clause_lengths)
        self.negation_probability = negation_probability
        self.logical_connectives = []
        self.variable_names = set(variable_names)

    def generate(self) -> Iterable[ptl.PTLFormula]:
        var_gen = ptl_gen.VariableGenerator(variable_names=self.variable_names)

        def generate_clause(length: int):
            return ptl.PTLFormula(children=[var_gen.generate() for _ in range(length)],
                                  logical_connective=LogicalConnective.OR)

        solver = Z3CNFConstraintSolver(
            clause_lengths=self.clause_lengths,
            number_of_clauses=self.number_of_clauses,
            number_of_literals=self.number_of_variables)
        for solution in solver.solve_in_random_order():
            root = ptl.PTLFormula(children=[], logical_connective=LogicalConnective.AND)
            random_unary_connective_generator = self._random_unary_connective_generator()
            for clause_len, amount_of_clauses in solution.items():
                for _ in range(amount_of_clauses):
                    clause = generate_clause(clause_len)
                    for variable in clause:
                        variable: ptl.Variable
                        variable.unary_connectives.extend(next(random_unary_connective_generator))
                        if self.negation_probability >= random.random():
                            variable.unary_connectives.append(LogicalConnective.NOT)
                    root.append(clause)
            yield root

    def _random_unary_connective_generator(self):
        original = {'variables_with_eventually_connectives': self.number_of_variables_with_eventually_connectives,
                    'variables_with_always_connectives': self.number_of_variables_with_always_connectives,
                    'variables_without_connective': self.number_of_variables_without_connective}
        values = {'variables_with_eventually_connectives': 0,
                  'variables_with_always_connectives': 0,
                  'variables_without_connective': 0}
        connectives_lookup = {'variables_with_eventually_connectives': [TemporalLogicConnective.EVENTUALLY],
                              'variables_with_always_connectives': [TemporalLogicConnective.ALWAYS],
                              'variables_without_connective': []}
        while True:
            connectives = {}
            # not we check if have minimal value
            for key in values.keys():
                if values[key] < original[key].min:
                    connectives[key] = connectives_lookup[key]
            # all keys reached minimal required value
            if not connectives:
                connectives = connectives_lookup.copy()
            # check if values are not too big
            for key in list(connectives.keys()):
                if values[key] > original[key].max:
                    del connectives[key]

            assert connectives
            random_key = random.choice(list(connectives.keys()))
            yield connectives[random_key]
            values[random_key] += 1

    @property
    def number_of_variables(self) -> IntegerRange:
        range_min = self.number_of_variables_without_connective.min + \
                    self.number_of_variables_with_eventually_connectives.min + \
                    self.number_of_variables_with_always_connectives.min
        range_max = self.number_of_variables_without_connective.max + \
                    self.number_of_variables_with_eventually_connectives.max + \
                    self.number_of_variables_with_always_connectives.max
        return IntegerRange(min=range_min, max=range_max)
