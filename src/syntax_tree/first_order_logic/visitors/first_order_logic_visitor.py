from __future__ import annotations

from .._atom import Atom
from .._formula import FOLFormula
from .._functor import Functor
from .._predicate import Predicate
from .._quantifier import Quantifier
from .._variable import Variable
from ..conjunctive_normal_form import CNFClause
from ..conjunctive_normal_form import CNFFOLFormula
from ...syntax_tree import FirstOrderLogicNode
from ...syntax_tree_visitor import SyntaxTreeVisitor


class FOLSyntaxTreeVisitor(SyntaxTreeVisitor):

    def visit(self, element: FirstOrderLogicNode):
        if isinstance(element, Variable):
            self.visit_variable(element)
        elif isinstance(element, Functor):
            self.visit_functor(element)
        elif isinstance(element, Predicate):
            self.visit_predicate(element)
        elif isinstance(element, Atom):
            self.visit_atom(element)
        elif isinstance(element, CNFClause):
            self.visit_cnf_clause(element)
        elif isinstance(element, FOLFormula):
            self.visit_formula(element)
        elif isinstance(element, Quantifier):
            self.visit_quantifier(element)
        elif isinstance(element, CNFFOLFormula):
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

    def visit_cnf_clause(self, element: CNFClause):
        pass

    def visit_cnf_formula(self, element: CNFFOLFormula):
        pass

    def visit_quantifier(self, element: Quantifier):
        pass

    def visit_formula(self, element: FOLFormula):
        pass
