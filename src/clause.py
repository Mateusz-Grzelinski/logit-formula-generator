import random
from abc import abstractmethod
from dataclasses import dataclass, field, InitVar
from operator import methodcaller
from typing import List, Optional, Dict

from src.literal import Literal, LiteralGenerator


@dataclass
class Clause:
    literals: List[Literal] = field(default_factory=list)

    def to_dimacs(self) -> str:
        return f"{' '.join(map(methodcaller('as_dimacs'), self.literals))} 0"


class ClauseGenerator:
    @property
    @abstractmethod
    def total_clauses(self) -> int:
        """:return total number of clauses that generator can produce"""

    @property
    @abstractmethod
    def clauses_left(self) -> int:
        """:return number of clauses that generator can still produce"""

    @property
    @abstractmethod
    def generated_clauses(self) -> int:
        """:return number of clauses that generator has produced"""

    @property
    @abstractmethod
    def new_clause(self) -> Optional[Clause]:
        """Generate new clause"""

    def __iter__(self):
        while True:
            if self.clauses_left != 0:
                yield self.new_clause
            else:
                break


class VariableLengthClauseGenerator(ClauseGenerator):
    """Generates exactly total_clauses by calling new_clause
    uses VariableGenerator to control number of variables
    generator is depleted when self.clauses_left == 0
    """

    def __init__(self, total_clauses: int, literal_gen: LiteralGenerator, max_clause_size: int = None):
        self.literal_gen = literal_gen
        self.max_clause_size = max_clause_size
        self._generated_clauses = 0
        self._total_clauses = total_clauses
        # this ensures that length of clause will be uniform
        if self.max_clause_size is None:
            self.max_clause_size = 2 * self.literal_gen.total_literals // self.total_clauses

        if self.literal_gen.literals_left < self.clauses_left:
            raise Exception("There are not enough variables in given variable generator, "
                            f"should be more than {self.clauses_left}")

        if self.literal_gen.literals_left > self.max_clause_size * self.total_clauses:
            raise Exception("There are too many variables in variable generator, "
                            f"should be less than {self.max_clause_size * self.total_clauses}")

    @property
    def total_clauses(self) -> int:
        return self._total_clauses

    @property
    def clauses_left(self) -> int:
        """:return number of clauses that generator can produce"""
        return self._total_clauses - self.generated_clauses

    @property
    def generated_clauses(self) -> int:
        """:return number of clauses that generator has produced"""
        return self._generated_clauses

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

            # cover case, there must be at least one literal per clause
            size = min(size, self.literal_gen.literals_left - self.clauses_left)

            # cover case, there are too many variables left for remaining clauses
            max_variables_consumed_by_remaining_clauses = (self.clauses_left - 1) * self.max_clause_size
            if self.literal_gen.literals_left - size > max_variables_consumed_by_remaining_clauses:
                size = self.literal_gen.literals_left - max_variables_consumed_by_remaining_clauses

        clause = Clause()
        for _ in range(size):
            literal = self.literal_gen.random_literal
            clause.literals.append(literal)
        self._generated_clauses += 1
        return clause


class KSATClauseGenerator(ClauseGenerator):

    def __init__(self, literal_gen: LiteralGenerator, k_clauses: Dict[int, int]):
        self.literal_gen = literal_gen
        # [k, required number of k clauses]
        self.k_clauses: Dict[int, int] = k_clauses
        self._required_literals = sum(k * number_of_k for k, number_of_k in k_clauses.items())
        self._total_clauses = sum(number_of_k for number_of_k in k_clauses.values())
        self._generated_clauses: int = 0

        if self.literal_gen.literals_left < self.clauses_left:
            raise Exception("There are not enough variables in given variable generator, "
                            f"should be more than {self.clauses_left}")

        # if self.literal_gen.literals_left > self._required_literals * self.total_clauses:
        #     raise Exception("There are too many variables in variable generator, "
        #                     f"should be less than {self._required_literals * self.total_clauses}")

    @property
    def total_clauses(self) -> int:
        return self._total_clauses

    @property
    def generated_clauses(self) -> int:
        return self._generated_clauses

    @property
    def new_clause(self) -> Optional[Clause]:
        if self.clauses_left == 0:
            return None

        next_clause_size = random.choice(list(self.k_clauses.keys()))
        if self.k_clauses[next_clause_size] == 1:
            del self.k_clauses[next_clause_size]
        else:
            self.k_clauses[next_clause_size] -= 1

        clause = Clause()
        for _ in range(next_clause_size):
            literal = self.literal_gen.random_literal
            clause.literals.append(literal)
        self._generated_clauses += 1
        return clause

    @property
    def clauses_left(self) -> int:
        """:return number of clauses that generator can produce"""
        return self._total_clauses - self.generated_clauses
