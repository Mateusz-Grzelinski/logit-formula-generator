import copy
import random
from typing import Iterable

import src.ast.propositional_temporal_logic as ptl
import src.generators.syntax_tree_generators.propositional_temporal_logic as ptl_gen
from src.ast import get_connective_properties, LogicalConnective
from src.generators import AstGenerator, IntegerRange
from src.generators.contraint_solver.first_order_logic.z3_solver import Z3CNFConstraintSolver


class CNFPropositionalTemporalLogicGenerator(AstGenerator):
    variable_name = 'v'

    def __init__(self, variable_names: Iterable[str],
                 number_of_variables_without_connective: IntegerRange,
                 number_of_variables_with_always_connectives: IntegerRange,
                 number_of_variables_with_eventually_connectives: IntegerRange,
                 number_of_clauses: IntegerRange,
                 clause_lengths: Iterable[int]) -> None:
        self.number_of_variables_without_connective = number_of_variables_without_connective
        self.number_of_variables_with_always_connectives = number_of_variables_with_always_connectives
        self.number_of_variables_with_eventually_connectives = number_of_variables_with_eventually_connectives
        self.number_of_clauses = number_of_clauses
        self.clause_lengths = set(clause_lengths)
        self.logical_connectives = []
        self.variable_names = set(variable_names)

    def generate(self) -> Iterable[ptl.PTLFormula]:
        var_gen = ptl_gen.VariableGenerator(variable_names=self.variable_names)

        def generate_clause(length: int):
            return ptl.PTLFormula(items=[var_gen.generate() for _ in range(length)],
                                  logical_connective=get_connective_properties(LogicalConnective.OR))

        solver = Z3CNFConstraintSolver(
            clause_lengths=self.clause_lengths,
            number_of_clauses=self.number_of_clauses,
            number_of_literals=self.number_of_variables)
        for solution in solver.solve_in_random_order():
            print(solution)
            root = ptl.PTLFormula(items=[], logical_connective=get_connective_properties(LogicalConnective.AND))
            random_unary_connective_generator = self._random_unary_connective_generator()
            for clause_len, amount_of_clauses in solution.items():
                for _ in range(amount_of_clauses):
                    clause = generate_clause(clause_len)
                    for variable in clause:
                        variable: ptl.Variable
                        variable.unary_connectives.extend(next(random_unary_connective_generator))
                    root.append(clause)
            yield root

    def _random_unary_connective_generator(self):
        original = {'variables_with_eventually_connectives': self.number_of_variables_with_eventually_connectives,
                    'variables_with_always_connectives': self.number_of_variables_with_always_connectives,
                    'variables_without_connective': self.number_of_variables_without_connective}
        values = {'variables_with_eventually_connectives': 0,
                  'variables_with_always_connectives': 0,
                  'variables_without_connective': 0}
        connectives = {'variables_with_eventually_connectives': [get_connective_properties('[]')],
                       'variables_with_always_connectives': [get_connective_properties('<>')],
                       'variables_without_connective': []}
        connectives_copy = copy.deepcopy(connectives)
        while True:
            connectives = copy.deepcopy(connectives_copy)
            # not we check if hawe minimal value
            for key in values.keys():
                if values[key] > original[key].min:
                    del connectives[key]
            # all keys reached minimul required value
            if not connectives:
                connectives = copy.deepcopy(connectives_copy)
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
