from __future__ import annotations

from collections.abc import Iterable

from .. import FirstOrderLogicFormula
from ...connectives import LogicalConnective


class CNFClause(FirstOrderLogicFormula):
    def __init__(self, children: Iterable[Atom] = None):
        super().__init__(children=children, binary_logical_connective=LogicalConnective.OR)

    def __str__(self):
        return 'cnf(name,axiom,' + '|'.join(str(l) for l in self) + ').'

    def equivalent(self, cnf_clause: CNFClause):
        """Compare 2 clauses but do not take into account order of literals"""
        for item in self:
            if item not in cnf_clause:
                return False
        return True

    def equivalent_in(self, cnf_clauses: Iterable[CNFClause]):
        for cnf_clause in cnf_clauses:
            if self.equivalent(cnf_clause):
                return True
        return False

    @property
    def length(self) -> int:
        return len(self)

    @property
    def is_unit(self) -> bool:
        return len(self) == 1

    @property
    def is_horn(self) -> bool:
        """A Horn clause is a clause (a disjunction of literals) with at most one positive, i.e. unnegated, literal"""
        from src.syntax_tree.first_order_logic import Atom
        positive_literals = 0
        for atom in self:
            atom: Atom
            if LogicalConnective.NOT in atom.unary_connectives:
                positive_literals += 1
        return positive_literals <= 1

    @property
    def number_of_singleton_variables(self) -> int:
        from src.syntax_tree.first_order_logic import Variable
        variables = list(self.recursive_nodes(type=Variable))
        singleton_vars = set([x for x in variables if variables.count(x) == 1])
        return len(singleton_vars)
