""" lfg - logic formula generator """
import random
from operator import methodcaller
from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple


def random_bool(probability: float = 0.5) -> bool:
    return random.random() < probability


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
    __variable_number: int = 0
    __generated_used_variables: int = 0

    def __post_init__(self):
        if self.unique_variables > self.total_variables:
            raise Exception("Number of total variables must be greater or equal to unique variables")

    @property
    def generated_variables(self) -> int:
        """:return number of generated variables"""
        return self.generated_unique_variables + self.__generated_used_variables

    @property
    def generated_unique_variables(self) -> int:
        """:return number of generated unique variables"""
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

        # there are no variables generated yet
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
        """Get random, arleady generated variable
        :return Variable or None when self.total_variables is hit
        """
        if not self.__variable_number:
            return None
        self.__generated_used_variables += 1

        return Variable(name=self.name, number=random.randint(0, self.__variable_number - 1))

    @property
    def new_variable(self) -> Optional[Variable]:
        """Generate new variable until self.unique_variables is hit
        :return new unique Variable, or None when self.unique_variables_left is 0
        """
        if not self.unique_variables_left:
            return None

        var = Variable(name=self.name, number=self.__variable_number)
        self.__variable_number += 1
        return var


@dataclass
class Clause:
    variables: List[Variable] = field(default_factory=list)

    def to_dimacs(self) -> str:
        return f"{' '.join(map(methodcaller('as_dimacs'), self.variables))} 0"


@dataclass
class ClauseGenerator:
    """Generates exactly total_clauses by calling new_clause
    uses VariableGenerator to control number of variables
    generator is depleted when self.clauses_left == 0
    """
    variable_gen: VariableGenerator
    total_clauses: int = 200
    max_clause_size: int = 100
    negate_probability: float = 0.5
    __generated_clauses: int = 0

    def __post_init__(self):
        if self.negate_probability < 0 or self.negate_probability > 1:
            raise Exception("negate_pobability range is [0, 1]")

        if self.variable_gen.variables_left < self.clauses_left:
            raise Exception("can not produce enough clauses with given variable generator")

        if self.max_clause_size * self.total_clauses < self.variable_gen.variables_left:
            print("warning: variable generator will not be completely depleted "
                  f"because of too small max_clause_size")

    @property
    def clauses_left(self) -> int:
        """:return number of clauses that generator can produce"""
        return self.total_clauses - self.__generated_clauses

    @property
    def generated_clauses(self) -> int:
        """:return number of clauses that generator has produced"""
        return self.__generated_clauses

    @property
    def new_clause(self) -> Optional[Clause]:
        """Generate new clause
        :return Clause or None, when
        """
        # generator depleted
        if self.clauses_left == 0:
            return None

        # help generator to end clause generation by putting all remaining variables to one clause
        if self.clauses_left == 1 and self.variable_gen.variables_left < self.max_clause_size:
            size = self.variable_gen.variables_left
        else:
            # cover case, there must be at least one variable per clause
            max_range = min(self.max_clause_size, self.variable_gen.variables_left - self.clauses_left)
            size = random.randint(1, max_range) if max_range != 0 else 1

            # cover case, there are too many variables left for remaining cases
            while self.variable_gen.variables_left - size > (self.clauses_left - 1) * self.max_clause_size:
                size += 1

        clause = Clause()
        for _ in range(size):
            variable = self.variable_gen.random_variable
            variable.negated = random_bool(self.negate_probability)
            clause.variables.append(variable)
        self.__generated_clauses += 1
        return clause


if __name__ == '__main__':
    clauses = 1000
    v = VariableGenerator("a", unique_variables=50, total_variables=2000)
    c = ClauseGenerator(variable_gen=v, total_clauses=1000, max_clause_size=100, negate_probability=0.1)
    print(f"p {c.total_clauses} {v.total_variables}")
    for i in range(clauses):
        print(c.new_clause.to_dimacs())
    # print("left clauses: ")
    # print(c.clauses_left)
    # print("left variables: ")
    # print(v.variables_left)
