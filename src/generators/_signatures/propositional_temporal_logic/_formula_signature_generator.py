import random
from typing import Generator, Any, Type, Union

import src.ast.propositional_temporal_logic as ptl
from src.generators import AstGenerator


class FormulaSignatureGenerator(AstGenerator):
    variable_name = 'v'

    def __init__(self, number_of_variables: int):
        self.number_of_variables = number_of_variables

    def generate(self) -> Generator[Union[ptl.Formula, Type[ptl.Formula]], Any, Any]:
        if self.number_of_variables == 1:
            return ptl.Formula(items=[ptl.Variable(name=self.variable_name)])
        else:
            return self._formula_signature_generator_helper(number_of_variables=self.number_of_variables)

    def _formula_signature_generator_helper(self, number_of_variables: int):
        if number_of_variables == 1:
            return ptl.Variable(name=self.variable_name)
        elif number_of_variables == 2:
            return ptl.Formula(items=[ptl.Variable(name=self.variable_name), ptl.Variable(name=self.variable_name)])
        else:
            left_subtree_size = random.randrange(1, number_of_variables)
            right_subtree_size = number_of_variables - left_subtree_size
            left_subtree = self._formula_signature_generator_helper(left_subtree_size)
            right_subtree = self._formula_signature_generator_helper(right_subtree_size)
            return ptl.Formula(items=[left_subtree, right_subtree])
