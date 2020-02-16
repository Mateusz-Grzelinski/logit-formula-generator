from __future__ import annotations

from typing import NoReturn

from src.syntax_tree import MathConnective
from ..first_order_logic_exporter import FirstOrderLogicExporter
from ..._atom import Atom
from ..._fol_formula import FirstOrderLogicFormula
from ..._functor import Functor
from ..._predicate import Predicate
from ..._quantifier import Quantifier
from ..._variable import Variable
from ...conjunctive_normal_form._cnf_clause import CNFClause


class TPTPExporter(FirstOrderLogicExporter):
    extension = '.p'

    def visit_pre(self, element: FirstOrderLogicNode) -> NoReturn:
        super().visit_pre(element)

    def visit_variable_pre(self, element: Variable):
        self.formula_buffer.write(element.name.capitalize())

    def visit_functor_pre(self, element: Functor):
        self.formula_buffer.write(element.name)
        if len(element):
            self.formula_buffer.write('(')

    def visit_predicate_pre(self, element: Predicate):
        self.formula_buffer.write(element.name)
        if len(element):
            self.formula_buffer.write('(')

    def visit_cnf_clause_pre(self, element: CNFClause):
        self.formula_buffer.write('cnf(name,axiom,')

    def visit_cnf_formula_pre(self, element: CNFFirstOrderLogicFormula):
        # write header here?
        super().visit_cnf_formula_pre(element)

    def visit_quantifier_pre(self, element: Quantifier):
        # todo
        super().visit_quantifier_pre(element)

    def visit_fol_formula_pre(self, element: FirstOrderLogicFormula):
        # todo introduce braces for each formula?
        # if this is root formula
        if not self.context:
            self.formula_buffer.write('fol(name,axiom,')
        if len(element) != 1:
            self.formula_buffer.write('(')

    def visit_functor_in_between_children(self, element: Functor):
        self.formula_buffer.write(',')

    def visit_predicate_in_between_children(self, element: Predicate):
        self.formula_buffer.write(',')

    def visit_atom_in_between_children(self, element: Atom):
        if MathConnective.EQUAL == element.math_connective:
            self.formula_buffer.write('=')
        elif MathConnective.EQUAL == element.math_connective:
            self.formula_buffer.write('!=')

    def visit_cnf_clause_in_between_children(self, element: CNFClause):
        # write logical OR
        self.formula_buffer.write('|')

    def visit_cnf_formula_in_between_children(self, element: CNFFirstOrderLogicFormula):
        # this is done in visit_cnf_clause_pre
        pass

    def visit_quantifier_in_between_children(self, element: Quantifier):
        super().visit_quantifier_in_between_children(element)

    def visit_fol_formula_in_between_children(self, element: FirstOrderLogicFormula):
        # write logical connective. Until default visualization is the taken from TPTP we are good
        self.formula_buffer.write(element.logical_connective.sign)

    def visit_functor_post(self, element: Functor):
        if len(element):
            self.formula_buffer.write(')')

    def visit_predicate_post(self, element: Predicate):
        if len(element):
            self.formula_buffer.write(')')

    def visit_cnf_clause_post(self, element: CNFClause):
        self.formula_buffer.write(').\n')

    def visit_quantifier_post(self, element: Quantifier):
        super().visit_quantifier_post(element)

    def visit_fol_formula_post(self, element: FirstOrderLogicFormula):
        if len(element) != 1:
            self.formula_buffer.write(')')
        if not self.context:
            self.formula_buffer.write(').')
        super().visit_fol_formula_post(element)
