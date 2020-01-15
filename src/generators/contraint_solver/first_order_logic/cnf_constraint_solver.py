import random
from abc import abstractmethod
from typing import Iterable, List, Dict

from src.generators.utils._range import IntegerRange


class CNFConstraintSolver:
    def __init__(self, allowed_clause_lengths: List, number_of_clauses: IntegerRange, number_of_literals: IntegerRange):
        self.literal_coefficients = allowed_clause_lengths
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
        if skip_chance > 0.5:
            skip_chance = 0.5
        cache = []
        for solution in self.solve():
            if random.random() < skip_chance:
                yield solution
            else:
                cache.append(solution)

        random.shuffle(cache)
        for cached_solution in cache:
            yield cached_solution
