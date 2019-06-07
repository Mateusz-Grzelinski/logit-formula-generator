import random
from dataclasses import dataclass
from typing import Optional

from src._common import random_bool


@dataclass
class Literal:
    name: str
    number: int = 0
    negated: bool = False

    def to_dimacs(self) -> str:
        return f'-{self.name}{self.number}' if self.negated else f'{self.name}{self.number}'

    def to_tptp(self) -> str:
        return f'~{self.name}{self.number}' if self.negated else f'{self.name}{self.number}'


@dataclass
class LiteralGenerator:
    """Generates exactly total_literals literals by appending number to name
    generator is depleted when self.literals_left == 0
    """
    name: str
    unique_literals: int = 100
    total_literals: int = 2_000
    negate_probability: float = 0.5
    _literal_number: int = 0
    _generated_used_literal: int = 0

    def __post_init__(self):
        if self.negate_probability < 0 or self.negate_probability > 1:
            raise Exception('negate_pobability range is [0, 1]')

        if self.unique_literals > self.total_literals:
            raise Exception('number of total literals must be greater or equal to unique literals')

    @property
    def generated_literals(self) -> int:
        """:return number of antlr_generated literals"""
        return self.generated_unique_literals + self._generated_used_literal

    @property
    def generated_unique_literals(self) -> int:
        """:return number of antlr_generated unique literals"""
        return self._literal_number

    @property
    def literals_left(self) -> int:
        """:return how many literals in total generator can produce"""
        return self.total_literals - self.generated_literals

    @property
    def unique_literals_left(self) -> int:
        """:return how many unique literals generator can produce"""
        return self.unique_literals - self.generated_unique_literals

    @property
    def random_literal(self) -> Optional[Literal]:
        """Get used or new Variable
        :return Variable or None, when can not generate neither new nor used Variable
        """
        # make sure all unique literals are always produced
        if self.unique_literals_left == self.literals_left:
            return self.new_literal

        # there are no literals antlr_generated yet
        if self.generated_literals == 0:
            return self.new_literal

        # actual random generating
        if self.unique_literals_left != 0:
            return self.used_literal if random_bool() else self.new_literal
        elif self.literals_left != 0:
            return self.used_literal
        else:
            return None

    @property
    def used_literal(self) -> Optional[Literal]:
        """Get random, arleady antlr_generated literal
        :return Variable or None when self.total_literals is hit
        """
        if not self._literal_number:
            return None
        self._generated_used_literal += 1

        return Literal(name=self.name,
                       number=random.randint(0, self._literal_number - 1),
                       negated=random_bool(self.negate_probability))

    @property
    def new_literal(self) -> Optional[Literal]:
        """Generate new variable until self.unique_literals is hit
        :return new unique Variable, or None when self.unique_literals_left is 0
        """
        if not self.unique_literals_left:
            return None

        var = Literal(name=self.name,
                      number=self._literal_number,
                      negated=random_bool(self.negate_probability))
        self._literal_number += 1
        return var
