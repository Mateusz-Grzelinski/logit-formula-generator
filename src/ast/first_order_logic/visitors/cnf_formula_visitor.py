from __future__ import annotations

from collections import defaultdict
from typing import Optional, Dict, Type, Set

from src.ast._connectives import MathConnective
from src.ast.first_order_logic._atom import Atom
from src.ast.first_order_logic._functor import Functor
from src.ast.first_order_logic._predicate import Predicate
from src.ast.first_order_logic._variable import Variable
from src.ast.first_order_logic.conjunctive_normal_form._cnf_clause import CNFClause
from src.ast.first_order_logic.conjunctive_normal_form._cnf_formula import CNFFormula
from src.ast.first_order_logic.conjunctive_normal_form._literal import Literal
from src.ast.first_order_logic.visitors import CNFFormulaInfo
from src.ast.first_order_logic.visitors.first_order_logic_visitor import FOLAstVisitor


class MathSense:
    @staticmethod
    def hash_variable(scope: Optional[CNFClause], variable: Variable) -> int:
        return hash((id(scope), variable.name))

    @staticmethod
    def hash_functor(functor: Functor) -> int:
        return hash(functor.name) ^ functor.arity

    @staticmethod
    def hash_predicate(predicate: Predicate) -> int:
        return hash((predicate.name, predicate.arity))

    @staticmethod
    def hash_atom(scope: Optional[CNFClause], atom: Atom) -> int:
        item_hashes = []
        for var in atom.items(type=Variable):
            item_hashes.append(MathSense.hash_variable(scope, var))
        for pred in atom.items(type=Predicate):
            item_hashes.append(MathSense.hash_predicate(pred))
        if atom.connective_properties:
            return hash((atom.connective_properties.connective, *item_hashes))
        else:
            return hash((*item_hashes,))

    @staticmethod
    def hash_literal(scope: Optional[CNFClause], literal: Literal) -> int:
        return hash((literal.is_negated, MathSense.hash_atom(scope, literal.atom)))

    @staticmethod
    def hash_clause(clause: CNFClause) -> int:
        return hash(tuple(MathSense.hash_literal(None, literal) for literal in clause._items))


# todo self.number_of[] does not work properly for all types
class CNFFormulaVisitor(FOLAstVisitor):
    def __init__(self):
        self.info = CNFFormulaInfo()
        self.info.clause_lengths = defaultdict(int)
        self.info.functor_arities = defaultdict(int)
        self.info.predicate_arities = defaultdict(int)
        self.info.term_instances_depths = defaultdict(int)
        # in future more advanced mechanism for context may be needed
        self.context: Optional[CNFClause] = None  # or quantifier
        self._hashes_in_math_sense: Dict[Type[FOLElement], Set[int]] = {}
        for element_type in [Variable, Functor, Predicate, Atom, Literal, CNFClause, CNFFormula]:
            self._hashes_in_math_sense[element_type.__name__] = set()
            self.info.number_of_instances[element_type.__name__] = 0
            self.info.number_of[element_type.__name__] = 0

    def visit(self, element: FOLElement):
        super().visit(element)

    def visit_variable(self, element: Variable):
        self._hashes_in_math_sense[Variable.__name__].add(MathSense.hash_variable(self.context, element))
        self.info.number_of_instances[Variable.__name__] += 1

    def visit_functor(self, element: Functor):
        self._hashes_in_math_sense[Functor.__name__].add(MathSense.hash_functor(element))
        self.info.number_of_instances[Functor.__name__] += 1
        self.info.number_of[Functor.__name__] = len(self._hashes_in_math_sense[Functor.__name__])
        self.info.functor_arities[element.arity] += 1
        self.info.term_instances_depths[element.recursion_depth] += 1

    def visit_predicate(self, element: Predicate):
        self._hashes_in_math_sense[Predicate.__name__].add(MathSense.hash_predicate(element))
        self.info.number_of[Predicate.__name__] = len(self._hashes_in_math_sense[Predicate.__name__])
        self.info.number_of_instances[Predicate.__name__] += 1
        self.info.predicate_arities[element.arity] += 1

    def visit_atom(self, element: Atom):
        self._hashes_in_math_sense[Atom.__name__].add(MathSense.hash_atom(self.context, element))
        self.info.number_of[Atom.__name__] = len(self._hashes_in_math_sense[Atom.__name__])
        self.info.number_of_instances[Atom.__name__] += 1
        if element.connective_properties and \
                element.connective_properties.connective in {MathConnective.EQUAL, MathConnective.NOT_EQUAL}:
            self.info.number_of_equality_atom_instances += 1

    def visit_literal(self, element: Literal):
        self._hashes_in_math_sense[Literal.__name__].add(MathSense.hash_literal(self.context, element))
        self.info.number_of[Literal.__name__] = len(self._hashes_in_math_sense[Literal.__name__])
        self.info.number_of_instances[Literal.__name__] += 1
        if element.is_negated:
            self.info.number_of_negated_literal_instances += 1

    def visit_cnf_clause(self, element: CNFClause):
        self._hashes_in_math_sense[CNFClause.__name__].add(MathSense.hash_clause(element))
        # variable is clause scoped
        self.info.number_of_singleton_variables += element.number_of_singleton_variables
        self.info.number_of_instances[CNFClause.__name__] += 1
        self.info.clause_lengths[element.length] += 1
        if element.is_horn:
            self.info.number_of_horn_clauses_instances += 1
        self.context = element

    def visit_cnf_formula(self, element: CNFFormula):
        self.info.number_of[CNFFormula.__name__] += 1
        self.info.number_of_instances[CNFFormula.__name__] += 1

        # instances can be handled here (but should they?)
