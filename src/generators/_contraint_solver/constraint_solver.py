import random
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, List, Dict

from src.generators._range import IntegerRange


@dataclass
class Coefficient:
    clauses_coeff: List[int] = field(default_factory=list)
    literal_coeff: List[int] = field(default_factory=list)

    def __post_init__(self):
        assert len(self.clauses_coeff) == len(self.literal_coeff)

    def __len__(self):
        return len(self.clauses_coeff)


class ConstraintSolver:
    def __init__(self, allowed_clause_lengths: List, number_of_clauses: IntegerRange, number_of_literals: IntegerRange):
        self.coefficients = Coefficient(clauses_coeff=[1] * len(allowed_clause_lengths),
                                        literal_coeff=allowed_clause_lengths)
        self.number_of_literals = number_of_literals
        self.number_of_clauses = number_of_clauses

    @abstractmethod
    def solve(self) -> Iterable[Dict[int, int]]:
        """Yields solutions for given constraints

        :returns dict with solution - key is clause length, value is number of clauses
        """
        raise NotImplementedError

    def solve_in_random_order(self, skip_chance: float = None):
        skip_chance = random.random() if skip_chance is None else skip_chance
        cache = []
        for solution in self.solve():
            if random.random() < skip_chance:
                yield solution
            else:
                cache.append(solution)

        random.shuffle(cache)
        for cached_solution in cache:
            yield cached_solution
