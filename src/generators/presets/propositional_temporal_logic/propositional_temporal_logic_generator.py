import copy
import random
from typing import Iterable

import src.generators.syntax_tree_generators.propositional_temporal_logic as ptl_gen
import src.syntax_tree.propositional_temporal_logic as ptl
from src.generators import SyntaxTreeGenerator
from src.syntax_tree import get_connective_properties


class PropositionalTemporalLogicGenerator(SyntaxTreeGenerator):
    variable_name = 'v'

    def __init__(self, variable_names: Iterable[str], number_of_variables_without_connective: int,
                 number_of_variables_with_always_connectives: int,
                 number_of_variables_with_eventually_connectives: int,
                 number_of_variables_with_both_connectives: int,
                 logical_connectives: Iterable[str]) -> None:
        self.logical_connectives = []
        for connective in logical_connectives:
            self.logical_connectives.append(get_connective_properties(connective))
        self.variable_names = set(variable_names)
        self.number_of = {
            'variables_with_both_connectives': number_of_variables_with_both_connectives,
            'variables_with_eventually_connectives': number_of_variables_with_eventually_connectives,
            'variables_with_always_connectives': number_of_variables_with_always_connectives,
            'variables_without_connective': number_of_variables_without_connective}
        self._connectives = {
            'variables_with_both_connectives': [get_connective_properties('[]'), get_connective_properties('<>')],
            'variables_with_eventually_connectives': [get_connective_properties('[]')],
            'variables_with_always_connectives': [get_connective_properties('<>')],
            'variables_without_connective': []}

    def generate(self) -> ptl.PTLFormula:
        number_of = copy.copy(self.number_of)
        for key, val in self.number_of.items():
            if not val:
                del number_of[key]

        var_gen = ptl_gen.VariableGenerator(variable_names=self.variable_names)
        formula_generator = ptl_gen.FormulaGenerator(var_gen=var_gen, number_of_variables=self.number_of_variables,
                                                     logical_connectives=self.logical_connectives)
        formula = formula_generator.generate()
        for variable in formula.items(type=ptl.Variable):
            variable: ptl.Variable
            key = random.choice(list(number_of))
            number_of[key] -= 1
            if number_of[key] == 0:
                del number_of[key]
            variable.unary_connectives.extend(self._connectives[key])
        return formula

    @property
    def number_of_variables(self):
        return sum(self.number_of.values())
