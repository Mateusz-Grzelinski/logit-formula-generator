""" lfg - logic formula generator """
import random
from dataclasses import dataclass, field
from operator import methodcaller
from typing import List, Optional

from src.literal import Literal, LiteralGenerator


@dataclass
class Clause:
    variables: List[Literal] = field(default_factory=list)

    def to_dimacs(self) -> str:
        return f"{' '.join(map(methodcaller('as_dimacs'), self.variables))} 0"


@dataclass
class ClauseGenerator:
    """Generates exactly total_clauses by calling new_clause
    uses VariableGenerator to control number of variables
    generator is depleted when self.clauses_left == 0
    """
    literal_gen: LiteralGenerator
    max_clause_size: int = None
    total_clauses: int = 200
    __generated_clauses: int = 0

    def __post_init__(self):
        # this ensures that length of clause will be uniform
        if self.max_clause_size is None:
            self.max_clause_size = 2 * self.literal_gen.total_literals // self.total_clauses

        if self.literal_gen.literals_left < self.clauses_left:
            raise Exception(f"There are not enough variables in given variable generator, "
                            f"should be more than {self.clauses_left}")

        if self.literal_gen.literals_left > self.max_clause_size * self.total_clauses:
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
        if self.clauses_left == 1 and self.literal_gen.literals_left < self.max_clause_size:
            size = self.literal_gen.literals_left
        else:
            size = random.randint(1, self.max_clause_size)

            # cover case, there must be at least one variable per clause
            size = min(size, self.literal_gen.literals_left - self.clauses_left)

            # cover case, there are too many variables left for remaining clauses
            max_variables_consumed_by_remaining_clauses = (self.clauses_left - 1) * self.max_clause_size
            if self.literal_gen.literals_left - size > max_variables_consumed_by_remaining_clauses:
                size = self.literal_gen.literals_left - max_variables_consumed_by_remaining_clauses

        clause = Clause()
        for _ in range(size):
            variable = self.literal_gen.random_literal
            clause.variables.append(variable)
        self.__generated_clauses += 1
        return clause
