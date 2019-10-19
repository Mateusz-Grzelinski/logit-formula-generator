from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, List, Dict

from src.generators.range import Range


@dataclass
class Coefficient:
    clauses_coeff: List[int] = field(default_factory=list)
    literal_coeff: List[int] = field(default_factory=list)

    def __post_init__(self):
        assert len(self.clauses_coeff) == len(self.literal_coeff)

    def __len__(self):
        return len(self.clauses_coeff)


@dataclass
class ClauseInfo:
    number_of_literals: int


class ConstraintSolver:
    def __init__(self, allowed_clause_lengths: List, number_of_clauses: Range, number_of_literals: Range):
        self.coefficients = Coefficient(clauses_coeff=[1] * len(allowed_clause_lengths),
                                        literal_coeff=allowed_clause_lengths)
        self.number_of_literals = number_of_literals
        self.number_of_clauses = number_of_clauses

    @abstractmethod
    def solve(self) -> Iterable[Dict[int, int]]:
        """Yields solutions for given constraints starting from most optimal"""
        raise NotImplementedError
