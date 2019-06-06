import random
from dataclasses import dataclass
from typing import Optional

from src._common import random_bool


@dataclass
class Variable:
    name: str
    number: int = 0
    negated: bool = False

    def as_dimacs(self) -> str:
        if self.negated:
            return f"-{self.name}{self.number}"
        return f"{self.name}{self.number}"


@dataclass
class VariableGenerator:
    """Generates exactly total_variables variables by appending number to name
    generator is depleted when self.variables_left == 0
    """
    name: str
    unique_variables: int = 100
    total_variables: int = 2_000_000
    negate_probability: float = 0.5
    __variable_number: int = 0
    __generated_used_variables: int = 0

    def __post_init__(self):
        if self.negate_probability < 0 or self.negate_probability > 1:
            raise Exception("negate_pobability range is [0, 1]")

        if self.unique_variables > self.total_variables:
            raise Exception("Number of total variables must be greater or equal to unique variables")

    @property
    def generated_variables(self) -> int:
        """:return number of antlr_generated variables"""
        return self.generated_unique_variables + self.__generated_used_variables

    @property
    def generated_unique_variables(self) -> int:
        """:return number of antlr_generated unique variables"""
        return self.__variable_number

    @property
    def variables_left(self) -> int:
        """:return how many variables in total generator can produce"""
        return self.total_variables - self.generated_variables

    @property
    def unique_variables_left(self) -> int:
        """:return how many unique variables generator can produce"""
        return self.unique_variables - self.generated_unique_variables

    @property
    def random_variable(self) -> Optional[Variable]:
        """Get used or new Variable
        :return Variable or None, when can not generate neither new nor used Variable
        """
        # make sure all unique variables are always produced
        if self.unique_variables_left == self.variables_left:
            return self.new_variable

        # there are no variables antlr_generated yet
        if self.generated_variables == 0:
            return self.new_variable

        # actual random generating
        if self.unique_variables_left != 0:
            return self.used_variable if random_bool() else self.new_variable
        elif self.variables_left != 0:
            return self.used_variable
        else:
            return None

    @property
    def used_variable(self) -> Optional[Variable]:
        """Get random, arleady antlr_generated variable
        :return Variable or None when self.total_variables is hit
        """
        if not self.__variable_number:
            return None
        self.__generated_used_variables += 1

        return Variable(name=self.name,
                        number=random.randint(0, self.__variable_number - 1),
                        negated=random_bool(self.negate_probability))

    @property
    def new_variable(self) -> Optional[Variable]:
        """Generate new variable until self.unique_variables is hit
        :return new unique Variable, or None when self.unique_variables_left is 0
        """
        if not self.unique_variables_left:
            return None

        var = Variable(name=self.name,
                       number=self.__variable_number,
                       negated=random_bool(self.negate_probability))
        self.__variable_number += 1
        return var
