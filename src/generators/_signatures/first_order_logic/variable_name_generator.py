import random
from typing import Iterable

from src.generators import AstGenerator


class VariableNameGenerator(AstGenerator):
    def __init__(self, variable_names: Iterable[str]):
        self.variable_names = list(variable_names)

    def generate(self) -> str:
        return random.choice(self.variable_names)
