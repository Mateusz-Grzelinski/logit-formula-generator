import random
from abc import abstractmethod
from dataclasses import dataclass, field
from math import ceil
from typing import List, Optional, Dict, Any

from src.literal import Literal, LiteralGenerator


@dataclass
class Clause:
    literals: List[Literal] = field(default_factory=list)

    def to_dimacs(self) -> str:
        literals_dimacs = (literal.to_dimacs() for literal in self.literals)
        return f'{" ".join(literals_dimacs)} 0'

    def to_tptp(self) -> str:
        literal_tptp = (literal.to_tptp() for literal in self.literals)
        return f'cnf(placeholder_name, axiom, ({" | ".join(literal_tptp)}) ).'


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

    def __init__(self, total_clauses: int, lit_gen_init_vars: Dict[str, Any] = None, max_clause_size: int = None):
        """
        :param total_clauses: number of clauses to generate
        :param if literal_gen is None, it will be created with default literal:clause ratio 2:1.
        if provided does not satisfy certain constrains, exception will be raised
        :param max_clause_size: if None, defaults to literal_gen.total_literals / 2, but not less than 1
        """
        self._generated_clauses = 0
        self._total_clauses = total_clauses
        # this ensures that length of clause will be uniform

        if self._total_clauses < 1:
            raise Exception('number of calsues to generate can not be less than 1')

        if lit_gen_init_vars is None:
            lit_gen_init_vars = {}
        if lit_gen_init_vars.get('total_literals') is None:
            # keep the default literal:clause ration 2:1
            lit_gen_init_vars['total_literals'] = self.total_clauses * 2
        if lit_gen_init_vars.get('name') is None:
            lit_gen_init_vars['name'] = 'p'

        self.literal_gen = LiteralGenerator(**lit_gen_init_vars)

        self.max_clause_size = ceil(
            self.literal_gen.total_literals / self._total_clauses) if max_clause_size is None else max_clause_size
        if self.max_clause_size < 1:
            self.max_clause_size = 1

        if self.literal_gen.literals_left < self.clauses_left:
            raise Exception('There are not enough variables in given variable generator, '
                            f'should be more than {self.clauses_left}')

        if self.literal_gen.literals_left > self.max_clause_size * self.total_clauses:
            raise Exception('There are too many variables in variable generator, '
                            f'should be less than {self.max_clause_size * self.total_clauses}')

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
            size = min(size, self.literal_gen.literals_left - self.clauses_left + 1)

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
    """Generate clauses in k-SAT format"""

    def __init__(self, k_clauses: Dict[int, int], lit_gen_init_vars: Dict[str, Any] = None):
        """
        :param k_clauses keys are k value (how many literals in clauses),
         the value is how many of this kind of clause to produce
        :param literal_gen is not provided, one will be automatically created with proper setting.
         if provided literal_gen does not satisfy certain constrains, exception will be raised
        """
        # [k, required number of k clauses]
        self.k_clauses: Dict[int, int] = k_clauses
        self._required_literals = sum(k * number_of_k for k, number_of_k in k_clauses.items())
        self._total_clauses = sum(number_of_k for number_of_k in k_clauses.values())
        self._max_clause_size = max(k for k in k_clauses.keys())
        self._generated_clauses: int = 0

        if lit_gen_init_vars is None:
            lit_gen_init_vars = {}
        if lit_gen_init_vars.get('total_literals') is None:
            lit_gen_init_vars['total_literals'] = self._required_literals
        if lit_gen_init_vars.get('name') is None:
            lit_gen_init_vars['name'] = 'p'

        # if literal_gen is None:
        self.literal_gen = LiteralGenerator(**lit_gen_init_vars)

        if self.literal_gen.literals_left != self._required_literals:
            raise Exception(f'literal generator should produce exactly {self._required_literals}')

    @property
    def max_clause_size(self):
        return self._max_clause_size

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
