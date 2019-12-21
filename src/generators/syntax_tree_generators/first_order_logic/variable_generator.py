import random
from typing import Iterable

from src.ast.first_order_logic import Variable
from src.generators import AstGenerator


class VariableGenerator(AstGenerator):
    def __init__(self, variable_names: Iterable[str]):
        self.variable_names = list(variable_names)

    def generate(self) -> Variable:
        return Variable(name=random.choice(self.variable_names))
