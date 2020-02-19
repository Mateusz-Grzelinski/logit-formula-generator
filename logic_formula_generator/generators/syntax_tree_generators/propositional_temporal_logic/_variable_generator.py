import random
from typing import Iterable

from logic_formula_generator.generators import SyntaxTreeGenerator
from logic_formula_generator.syntax_tree.propositional_temporal_logic import Variable


class VariableGenerator(SyntaxTreeGenerator):
    def __init__(self, variable_names: Iterable[str]):
        self.variable_names = list(variable_names)

    def generate(self) -> Variable:
        return Variable(name=random.choice(self.variable_names), unary_connectives=[])
