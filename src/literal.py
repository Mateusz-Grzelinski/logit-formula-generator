import random
from abc import abstractmethod
from dataclasses import dataclass
from math import ceil
from typing import Optional, List, Union

from src._common import random_bool


@dataclass
class Literal:
    name: str
    number: int = 0
    negated: bool = False

    def __hash__(self) -> int:
        return hash((self.name, self.number, self.negated))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.number == other.number and self.negated == other.negated

    def to_dimacs(self) -> str:
        return f'-{self.name}{self.number}' if self.negated else f'{self.name}{self.number}'

    def to_tptp(self) -> str:
        return f'~{self.name}{self.number}' if self.negated else f'{self.name}{self.number}'


class LiteralGenerator:
    def generate(self) -> List[Literal]:
        return [i for i in iter(self)]

    def __iter__(self):
        while True:
            if self.literals_left != 0:
                yield self.literal
            else:
                break

    @property
    @abstractmethod
    def total_literals(self) -> int:
        pass

    @property
    @abstractmethod
    def generated_literal(self) -> int:
        """:return number of antlr_generated literals"""
        pass

    @property
    def literals_left(self) -> int:
        """:return how many literals in total generator can produce"""
        return self.total_literals - self.generated_literal

    @property
    @abstractmethod
    def literal(self) -> Optional[Literal]:
        """Get used or new Variable
        :return Variable or None, when can not generate neither new nor used Variable
        """
        pass

    @property
    @abstractmethod
    def negate_probability(self) -> float:
        pass


class RandomLiteralGenerator(LiteralGenerator):
    """Generates exactly total_literals literals by appending number to name
    generator is depleted when self.literals_left == 0
    """

    @property
    def negate_probability(self) -> float:
        return self._negate_probability

    def __init__(self, total_literals: int, name: str = 'p', unique_literals: Union[int, float] = None,
                 negate_probability: float = 0.5):
        """
        :param total_literals: how many literals to produce
        :param name: prefix of literal
        :param unique_literals: how many different literals to produce, either fixed value or percentage
        :param negate_probability: what percent of literals should be negated [0.0 to 1.0]
        """
        self._name = name
        self._total_literals = total_literals
        self._negate_probability = negate_probability
        self._literal_number = 0
        self._generated_used_literal = 0

        if unique_literals is None:
            self._unique_literals = total_literals
        elif 0 <= unique_literals < 1:
            self._unique_literals = ceil(total_literals * unique_literals)
        elif unique_literals >= 1:
            self._unique_literals = int(unique_literals)

        if not 0 <= self._negate_probability <= 1:
            raise Exception('negate_pobability range is [0, 1]')

        if self._unique_literals < 1:
            raise Exception('number of unique literals can not be less than 1')

        if self._total_literals < 1:
            raise Exception('number of literals to generate can not be less than 1')

        if self._unique_literals > self._total_literals:
            raise Exception('number of total literals must be greater or equal to unique literals')

    @property
    def total_literals(self) -> int:
        return self._total_literals

    @property
    def unique_literals(self) -> int:
        return self._unique_literals

    @property
    def generated_literal(self) -> int:
        """:return number of antlr_generated literals"""
        return self.generated_unique_literals + self._generated_used_literal

    @property
    def generated_unique_literals(self) -> int:
        """:return number of antlr_generated unique literals"""
        return self._literal_number

    @property
    def unique_literals_left(self) -> int:
        """:return how many unique literals generator can produce"""
        return self._unique_literals - self.generated_unique_literals

    @property
    def literal(self) -> Optional[Literal]:
        """Get used or new Variable
        :return Variable or None, when can not generate neither new nor used Variable
        """
        # make sure all unique literals are always produced
        if self.unique_literals_left == self.literals_left:
            return self.new_literal

        # there are no literals antlr_generated yet
        if self.generated_literal == 0:
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

        return Literal(name=self._name,
                       number=random.randint(0, self._literal_number - 1),
                       negated=random_bool(self._negate_probability))

    @property
    def new_literal(self) -> Optional[Literal]:
        """Generate new variable until self.unique_literals is hit
        :return new unique Variable, or None when self.unique_literals_left is 0
        """
        if not self.unique_literals_left:
            return None

        var = Literal(name=self._name,
                      number=self._literal_number,
                      negated=random_bool(self._negate_probability))
        self._literal_number += 1
        return var


class LiteralPicker(LiteralGenerator):

    @property
    def negate_probability(self) -> float:
        return self._negate_probability

    def __init__(self, literals: List[Literal], total_literals):
        self.literals = literals
        self._negate_probability = len([i for i in literals if i.negated]) / len(literals)
        self._total_literals = total_literals
        self._generated_literals = 0

    @property
    def total_literals(self) -> int:
        return self._total_literals

    @property
    def generated_literal(self) -> int:
        return self._generated_literals

    @property
    def literal(self) -> Optional[Literal]:
        if self.literals_left == 0:
            return None

        self._generated_literals += 1
        return random.choice(self.literals)
