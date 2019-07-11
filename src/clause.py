import random
from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from math import ceil
from typing import List, Optional, Dict, Set, Union

from src.literal import Literal, LiteralGenerator, RandomLiteralGenerator


@dataclass
class Clause:
    literals: Set[Literal] = field(default_factory=set)

    def to_dimacs(self) -> str:
        literals_dimacs = (literal.to_dimacs() for literal in self.literals)
        return f'{" ".join(literals_dimacs)} 0'

    def to_tptp(self) -> str:
        literal_tptp = (literal.to_tptp() for literal in self.literals)
        return f'cnf(placeholder_name, axiom, ({" | ".join(literal_tptp)}) ).'

    def __hash__(self) -> int:
        return hash(i for i in self.literals)


class ClauseGenerator:
    @property
    @abstractmethod
    def total_clauses(self) -> int:
        """:return total number of clauses that generator can produce"""

    @property
    def clauses_left(self) -> int:
        """:return number of clauses that generator can still produce"""
        return self.total_clauses - self.generated_clauses

    @property
    @abstractmethod
    def generated_clauses(self) -> int:
        """:return number of clauses that generator has produced"""

    @property
    @abstractmethod
    def clause(self) -> Optional[Clause]:
        """Generate new clause"""

    def generate(self) -> List[frozenset]:
        return [i for i in iter(self)]

    def __iter__(self):
        while True:
            if self.clauses_left != 0:
                yield self.clause
            else:
                break


class KSATClauseGenerator(ClauseGenerator):
    """Generate clauses in k-SAT format"""

    def __init__(self, k_clauses: Union[Dict[int, int], str], literal_gen: LiteralGenerator = None,
                 total_clauses: int = None, max_clause_size: int = None):
        self._generated_clauses = set()

        if literal_gen is None:
            # keep the default literal:clause ration 2:1
            self.literal_gen = KSATClauseGenerator._default_literal_generator(total_literals=total_clauses * 2)
        else:
            self.literal_gen = literal_gen

        if isinstance(k_clauses, dict):
            if total_clauses is not None:
                raise Exception('todo')
            if max_clause_size is not None:
                raise Exception('todo')

            self._total_clauses = sum(number_of_k for number_of_k in self.k_clauses.values())
            self.k_clauses: Dict[int, int] = k_clauses
            KSATClauseGenerator._check_literal_generator_constraints(self.literal_gen, self.total_clauses,
                                                                     self.max_clause_size)

        elif k_clauses == 'random':
            if total_clauses is None:
                raise Exception('todo')

            if total_clauses < 1:
                raise Exception('number of clauses to generate can not be less than 1')

            if max_clause_size is None:
                max_clause_size = ceil(self.literal_gen.total_literals / total_clauses) * 2
            elif max_clause_size < 1:
                raise Exception('max_clause_size can not be less than 1')

            KSATClauseGenerator._check_literal_generator_constraints(self.literal_gen, total_clauses, max_clause_size)

            self._total_clauses = total_clauses
            self.k_clauses = defaultdict(int)
            # take literal_gen.total_literals into consideration
            while total_clauses != 0:
                # help generator to end clause generation by putting all remaining variables to one clause
                if total_clauses == 1 and self.literal_gen.literals_left < max_clause_size:
                    k = self.literal_gen.literals_left
                else:
                    k = random.randint(1, max_clause_size)

                    # cover case, when there must be at least one literal per clause
                    k = min(k, self.literal_gen.total_literals - self.required_literals - total_clauses + 1)

                    # cover case, when there are too many variables left for remaining clauses
                    max_variables_consumed_by_remaining_clauses = (total_clauses - 1) * max_clause_size
                    if self.literal_gen.total_literals - self.required_literals - k > max_variables_consumed_by_remaining_clauses:
                        k = self.literal_gen.total_literals - self.required_literals - max_variables_consumed_by_remaining_clauses

                total_clauses -= 1
                self.k_clauses[k] += 1
        else:
            raise Exception('unknown value of k_clause')

        assert self.literal_gen.total_literals == self.required_literals

    @staticmethod
    def _check_literal_generator_constraints(literal_gen, total_clauses, max_clause_size):
        if literal_gen.total_literals < total_clauses:
            raise Exception('There are not enough variables in given variable generator, '
                            f'should be more than {total_clauses}. There must be at least one literal per clause')
        if literal_gen.total_literals > max_clause_size * total_clauses:
            raise Exception('There are too many variables in variable generator, '
                            f'should be less than {max_clause_size * total_clauses}')

    @staticmethod
    def _default_literal_generator(total_literals: int):
        return RandomLiteralGenerator(total_literals=total_literals,
                                      name='p',
                                      unique_literals=0.75,
                                      negate_probability=0.5)

    @property
    def total_clauses(self):
        return self._total_clauses

    @property
    def max_clause_size(self):
        return max(k for k in self.k_clauses.keys())

    @property
    def required_literals(self):
        return sum(k * number_of_k for k, number_of_k in self.k_clauses.items())

    @property
    def generated_clauses(self) -> int:
        return len(self._generated_clauses)

    @property
    def clause(self) -> Optional[Clause]:
        if self.clauses_left == 0:
            return None

        keys = list(self.k_clauses.keys())
        while True:
            next_clause_size = random.choice(keys)

            clause = Clause(literals={self.literal_gen.literal for _ in range(next_clause_size)})
            if clause not in self._generated_clauses:
                self._generated_clauses.add(clause)
                self.k_clauses[next_clause_size] -= 1
                if self.k_clauses[next_clause_size] == 0:
                    del self.k_clauses[next_clause_size]
                return clause
