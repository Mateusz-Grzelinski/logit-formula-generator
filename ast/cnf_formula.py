from typing import List

from .ast_element import AstElement
from .cnf_clause import CNFClause
from .containers import CNFClauseContainer


class CNFFormula(CNFClauseContainer, AstElement):
    def __init__(self, clauses: List[CNFClause]):
        super().__init__(additional_containers=[], items=clauses)

    def __str__(self):
        return '\n'.join(str(c) for c in self.clauses())
