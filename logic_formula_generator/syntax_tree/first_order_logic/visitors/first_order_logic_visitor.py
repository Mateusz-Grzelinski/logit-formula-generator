from __future__ import annotations

from typing import NoReturn

from ...syntax_tree import FirstOrderLogicNode
from ...syntax_tree_visitor import SyntaxTreeVisitor


class FirstOrderLogicSyntaxTreeVisitor(SyntaxTreeVisitor):
    def __init__(self):
        self.context = []

    def visit_pre(self, element: FirstOrderLogicNode) -> NoReturn:
        from .._atom import Atom
        from .._fol_formula import FirstOrderLogicFormula
        from .._functor import Functor
        from .._predicate import Predicate
        from .._quantifier import Quantifier
        from .._variable import Variable
        if isinstance(element, Variable):
            self.visit_variable_pre(element)
        elif isinstance(element, Functor):
            self.visit_functor_pre(element)
        elif isinstance(element, Predicate):
            self.visit_predicate_pre(element)
        elif isinstance(element, Atom):
            self.visit_atom_pre(element)
        elif isinstance(element, FirstOrderLogicFormula):
            self.visit_fol_formula_pre(element)
        elif isinstance(element, Quantifier):
            self.visit_quantifier_pre(element)
        else:
            assert False, f'Unknown element for visitor {type(element)}, {element}'
        self.context.append(element)

    def visit_in_between_children(self, element: SyntaxTreeNode) -> NoReturn:
        from .._atom import Atom
        from .._fol_formula import FirstOrderLogicFormula
        from .._functor import Functor
        from .._predicate import Predicate
        from .._quantifier import Quantifier
        from .._variable import Variable
        if isinstance(element, Variable):
            self.visit_variable_in_between_children(element)
        elif isinstance(element, Functor):
            self.visit_functor_in_between_children(element)
        elif isinstance(element, Predicate):
            self.visit_predicate_in_between_children(element)
        elif isinstance(element, Atom):
            self.visit_atom_in_between_children(element)
        elif isinstance(element, FirstOrderLogicFormula):
            self.visit_fol_formula_in_between_children(element)
        elif isinstance(element, Quantifier):
            self.visit_quantifier_in_between_children(element)
        else:
            assert False, f'Unknown element for visitor {type(element)}, {element}'

    def visit_post(self, element: FirstOrderLogicNode) -> NoReturn:
        from .._atom import Atom
        from .._fol_formula import FirstOrderLogicFormula
        from .._functor import Functor
        from .._predicate import Predicate
        from .._quantifier import Quantifier
        from .._variable import Variable
        self.context.pop()
        if isinstance(element, Variable):
            self.visit_variable_post(element)
        elif isinstance(element, Functor):
            self.visit_functor_post(element)
        elif isinstance(element, Predicate):
            self.visit_predicate_post(element)
        elif isinstance(element, Atom):
            self.visit_atom_post(element)
        elif isinstance(element, FirstOrderLogicFormula):
            self.visit_fol_formula_post(element)
        elif isinstance(element, Quantifier):
            self.visit_quantifier_post(element)
        else:
            assert False, f'Unknown element for visitor {type(element)}, {element}'

    def visit_variable_pre(self, element: Variable):
        pass

    def visit_functor_pre(self, element: Functor):
        pass

    def visit_predicate_pre(self, element: Predicate):
        pass

    def visit_atom_pre(self, element: Atom):
        pass

    def visit_quantifier_pre(self, element: Quantifier):
        pass

    def visit_fol_formula_pre(self, element: FirstOrderLogicFormula):
        pass

    def visit_variable_in_between_children(self, element: Variable):
        pass

    def visit_functor_in_between_children(self, element: Functor):
        pass

    def visit_predicate_in_between_children(self, element: Predicate):
        pass

    def visit_atom_in_between_children(self, element: Atom):
        pass

    def visit_quantifier_in_between_children(self, element: Quantifier):
        pass

    def visit_fol_formula_in_between_children(self, element: FirstOrderLogicFormula):
        pass

    def visit_variable_post(self, element: Variable):
        pass

    def visit_functor_post(self, element: Functor):
        pass

    def visit_predicate_post(self, element: Predicate):
        pass

    def visit_atom_post(self, element: Atom):
        pass

    def visit_quantifier_post(self, element: Quantifier):
        pass

    def visit_fol_formula_post(self, element: FirstOrderLogicFormula):
        pass
