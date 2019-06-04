""" lfg - logic formula generator """
import random
from dataclasses import dataclass, field
from operator import methodcaller
from typing import List, Optional

from src.variable import Variable, VariableGenerator


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
    max_clause_size: int = None
    total_clauses: int = 200
    __generated_clauses: int = 0

    def __post_init__(self):
        # this ensures that length of clause will be uniform
        if self.max_clause_size is None:
            self.max_clause_size = 2 * self.variable_gen.total_variables // self.total_clauses

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
