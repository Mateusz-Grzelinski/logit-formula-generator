from __future__ import annotations

from .._atom import Atom
from .._formula import FOLFormula
from .._functor import Functor
from .._predicate import Predicate
from .._quantifier import Quantifier
from .._variable import Variable
from ..conjunctive_normal_form import CNFClause
from ..conjunctive_normal_form import CNFFormula
from ..conjunctive_normal_form import Literal
from ..._ast_visitor import AstVisitor


class FOLAstVisitor(AstVisitor):

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
        elif isinstance(element, FOLFormula):
            self.visit_formula(element)
        elif isinstance(element, Quantifier):
            self.visit_quantifier(element)
        elif isinstance(element, CNFFormula):
            self.visit_cnf_formula(element)
        else:
            assert False, f'Unknown element for visitor {type(element)}, {element}'

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

    def visit_quantifier(self, element: Quantifier):
        pass

    def visit_formula(self, element: FOLFormula):
        pass
