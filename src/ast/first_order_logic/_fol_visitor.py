from __future__ import annotations

from src.ast._visitor import _Visitor
from src.ast.first_order_logic import Variable, Functor, Predicate, Atom, Literal, CNFClause, CNFFormula


class FOLVisitor(_Visitor):

    def visit(self, element: AstElement):
        if isinstance(element, Variable):
            self.visit_variable(element)
        elif isinstance(element, Functor):
            self.visit_functor(element)
        elif isinstance(element, Predicate):
            self.visit_predicate(element)
        elif isinstance(element, Atom):
            self.visit_atom(element)
        elif isinstance(element, Literal):
            self.visit_literal(element)
        elif isinstance(element, CNFClause):
            self.visit_cnf_clause(element)
        elif isinstance(element, CNFFormula):
            self.visit_cnf_formula(element)
        else:
            assert False, 'Unknown element for visitor'

    def visit_variable(self, element: Variable):
        pass

    def visit_functor(self, element: Functor):
        pass

    def visit_predicate(self, element: Predicate):
        pass

    def visit_atom(self, element: Atom):
        pass

    def visit_literal(self, element: Literal):
        pass

    def visit_cnf_clause(self, element: CNFClause):
        pass

    def visit_cnf_formula(self, element: CNFFormula):
        pass
