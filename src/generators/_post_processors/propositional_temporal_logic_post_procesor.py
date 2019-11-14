# should post processor be visitor?
import random
from typing import Iterable

import src.ast.propositional_temporal_logic as plt
from ._post_processor import PostProcessor


class PropositionalTemporalLogicPostProcessor(PostProcessor):
    def __init__(self, variable_names: Iterable[str], number_of_variables_with_both_connectives: int,
                 number_of_variables_with_eventually_connectives: int, number_of_variables_with_always_connectives: int,
                 number_of_variables_without_connective: int):
        self.variable_names = set(variable_names)
        self.number_of_variables_with_both_connectives = number_of_variables_with_both_connectives
        self.number_of_variables_with_eventually_connectives = number_of_variables_with_eventually_connectives
        self.number_of_variables_with_always_connectives = number_of_variables_with_always_connectives
        self.number_of_variables_without_connective = number_of_variables_without_connective

    def post_process(self, formula: plt.Formula):
        self.switch_names(formula)
        self.add_unary_connectives(formula)

    def switch_names(self, formula: plt.Formula):
        for variable in formula.items(type=plt.Variable):
            variable: plt.Variable
            variable.name = random.sample(self.variable_names, 1)[0]

    def add_unary_connectives(self, formula: plt.Formula):
        # todo implement
        pass
