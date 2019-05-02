""" lfg - logic formula generator """
import random
from operator import methodcaller
from dataclasses import dataclass, field, InitVar
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
    max_clause_size: InitVar[int] = None
    total_clauses: int = 200
    __generated_clauses: int = 0

    def __post_init__(self, max_clause_size):
        # this ensures that length of clause will be uniform
        if max_clause_size is None:
            self.max_clause_size = 2*self.variable_gen.total_variables // self.total_clauses

        if self.variable_gen.variables_left < self.clauses_left:
            raise Exception(f"There are not enough variables in given variable generator, "
                            f"should be more than {self.clauses_left}")

        if self.variable_gen.variables_left > self.max_clause_size * self.total_clauses:
            raise Exception(f"There are too many variables in variable generator, "
                            f"should be less than {self.max_clause_size * self.total_clauses}")

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
            size = random.randint(1, self.max_clause_size)

            # cover case, there must be at least one variable per clause
            size = min(size, self.variable_gen.variables_left - self.clauses_left)

            # cover case, there are too many variables left for remaining clauses
            max_variables_consumed_by_remaining_clauses = (self.clauses_left - 1) * self.max_clause_size
            if self.variable_gen.variables_left - size > max_variables_consumed_by_remaining_clauses:
                size = self.variable_gen.variables_left - max_variables_consumed_by_remaining_clauses

        clause = Clause()
        for _ in range(size):
            variable = self.variable_gen.random_variable
            clause.variables.append(variable)
        self.__generated_clauses += 1
        return clause


if __name__ == '__main__':
    clauses = 10
    v = VariableGenerator(name="a",
                          unique_variables=5,
                          total_variables=200,
                          negate_probability=0.1)
    c = ClauseGenerator(variable_gen=v,
                        total_clauses=10,
                        )
    print(f"p {c.total_clauses} {v.total_variables}")
    # print(c.new_clause.to_dimacs())
    for i in range(clauses):
        print(c.new_clause.to_dimacs())
    print("left clauses: ")
    print(c.clauses_left)
    print("left variables: ")
    print(v.variables_left)
