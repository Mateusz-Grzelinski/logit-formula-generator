import random
from typing import Iterable, Union

import src.ast.propositional_temporal_logic as ptl
from src.ast import ConnectiveProperties
from src.generators import AstGenerator
from ._variable_generator import VariableGenerator


class FormulaGenerator(AstGenerator):
    def __init__(self, var_gen: VariableGenerator, number_of_variables: int,
                 logical_connectives: Iterable[ConnectiveProperties]):
        self.logical_connective = list(logical_connectives)
        self.variable_gen = var_gen
        self.number_of_variables = number_of_variables

    def generate(self) -> ptl.PTLFormula:
        return self._formula_signature_generator_helper(number_of_variables=self.number_of_variables)

    def _formula_signature_generator_helper(self, number_of_variables: int) -> Union[ptl.PTLFormula, ptl.Variable]:
        if number_of_variables == 1:
            # todo: is single variable (not wrapped in formula) acceptable?
            return self.variable_gen.generate()
        elif number_of_variables == 2:
            return ptl.PTLFormula(items=[self.variable_gen.generate(), self.variable_gen.generate()],
                                  logical_connective=random.choice(self.logical_connective))
        else:
            left_subtree_size = random.randrange(1, number_of_variables)
            left_subtree = self._formula_signature_generator_helper(number_of_variables=left_subtree_size)
            right_subtree_size = number_of_variables - left_subtree_size
            right_subtree = self._formula_signature_generator_helper(number_of_variables=right_subtree_size)
            return ptl.PTLFormula(items=[left_subtree, right_subtree],
                                  logical_connective=random.choice(self.logical_connective))
