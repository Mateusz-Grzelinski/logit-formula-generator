from __future__ import annotations

import random
from typing import Iterable, Union, Dict

import src.syntax_tree.propositional_temporal_logic as ptl
from src.generators import SyntaxTreeGenerator
from src.syntax_tree import ConnectiveProperties
from src.syntax_tree import TemporalLogicConnective
from ._variable_generator import VariableGenerator


class FormulaGenerator(SyntaxTreeGenerator):
    def __init__(self, var_gen: VariableGenerator, number_of_variables: int,
                 logical_connectives: Iterable[ConnectiveProperties],
                 formula_subgenerators: Dict[TemporalLogicConnective, FormulaGenerator]):
        self.formula_subgenerators = formula_subgenerators
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
            return ptl.PTLFormula(children=[self.variable_gen.generate(), self.variable_gen.generate()],
                                  logical_connective=random.choice(self.logical_connective))
        else:
            left_subtree_size = random.randrange(1, number_of_variables)
            left_subtree = self._formula_signature_generator_helper(number_of_variables=left_subtree_size)
            right_subtree_size = number_of_variables - left_subtree_size
            right_subtree = self._formula_signature_generator_helper(number_of_variables=right_subtree_size)
            return ptl.PTLFormula(children=[left_subtree, right_subtree],
                                  logical_connective=random.choice(self.logical_connective))

    def cnf_efficient_formula_gen(self):
        formula = ptl.PTLFormula(children=[], logical_connective=TemporalLogicConnective.ALWAYS)
        memoize = []

        for i in self.number_of_clauses:
            pass
