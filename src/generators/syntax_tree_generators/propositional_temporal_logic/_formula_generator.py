import random

import src.ast.propositional_temporal_logic as ptl
from src.generators import AstGenerator
from ._variable_generator import VariableGenerator


class FormulaGenerator(AstGenerator):
    variable_name = 'v'

    def __init__(self, var_gen: VariableGenerator, number_of_variables: int):
        self.variable_gen = var_gen
        self.number_of_variables = number_of_variables

    def generate(self) -> ptl.Formula:
        return self._formula_signature_generator_helper(number_of_variables=self.number_of_variables)

    def _formula_signature_generator_helper(self, number_of_variables: int) -> ptl.Formula:
        if number_of_variables == 1:
            # todo: is single variable (not wrapped in formula) acceptable?
            return self.variable_gen.generate()
        elif number_of_variables == 2:
            return ptl.Formula(items=[self.variable_gen.generate(), self.variable_gen.generate()])
        else:
            left_subtree_size = random.randrange(1, number_of_variables)
            left_subtree = self._formula_signature_generator_helper(number_of_variables=left_subtree_size)
            right_subtree_size = number_of_variables - left_subtree_size
            right_subtree = self._formula_signature_generator_helper(number_of_variables=right_subtree_size)
            return ptl.Formula(items=[left_subtree, right_subtree])
