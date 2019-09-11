from statistics import mean
from typing import List

from .ast_element import AstElement
from .cnf_clause import CNFClause
from .containers import CNFClauseContainer


class CNFFormula(CNFClauseContainer, AstElement):
    def __init__(self, clauses: List[CNFClause], mutable=True):
        super().__init__(additional_containers=[], items=clauses, mutable=mutable)

    def __str__(self):
        return '\n'.join(str(c) for c in self.clauses())

    @property
    def number_of_variables(self) -> int:
        return sum(clause.number_of_variables for clause in self.clauses())

    @property
    def number_of_variable_instances(self) -> int:
        return sum(clause.number_of_variable_instances for clause in self.clauses())

    @property
    def max_clause_size(self):
        return max(clause.length for clause in self.clauses())

    @property
    def average_clause_size(self):
        return mean(clause.length for clause in self.clauses())

    @property
    def number_of_unit_clauses(self):
        return len(list(c for c in self.clauses() if c.is_unit))
