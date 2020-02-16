from __future__ import annotations

from collections import defaultdict
from typing import Optional, Dict, Set

from src.data_model._cnf_fol_formula_info import CNFFOLFormulaInfo
from src.syntax_tree import MathConnective, LogicalConnective
from src.syntax_tree.first_order_logic._atom import Atom
from src.syntax_tree.first_order_logic._functor import Functor
from src.syntax_tree.first_order_logic._predicate import Predicate
from src.syntax_tree.first_order_logic._variable import Variable
from src.syntax_tree.first_order_logic.conjunctive_normal_form._cnf_clause import CNFClause
from src.syntax_tree.first_order_logic.visitors.first_order_logic_visitor import FirstOrderLogicSyntaxTreeVisitor


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
        for var in atom.recursive_nodes(type=Variable):
            item_hashes.append(MathSense.hash_variable(scope, var))
        for pred in atom.recursive_nodes(type=Predicate):
            item_hashes.append(MathSense.hash_predicate(pred))
        if atom.math_connective:
            return hash((atom.math_connective.connective, *item_hashes))
        else:
            return hash((*item_hashes,))

    @staticmethod
    def hash_clause(clause: CNFClause) -> int:
        return hash(tuple(MathSense.hash_atom(None, atom) for atom in clause))


class CNFFormulaInfoCollector(FirstOrderLogicSyntaxTreeVisitor):
    def __init__(self):
        super().__init__()
        self.info = CNFFOLFormulaInfo()
        self.info.clause_lengths = defaultdict(int)
        self.info.functor_arities = defaultdict(int)
        self.info.predicate_arities = defaultdict(int)
        self.info.term_instances_depths = defaultdict(int)
        # in future more advanced mechanism for context may be needed
        self.last_visited_cnf_clause: Optional[CNFClause] = None  # or quantifier
        self._hashes_in_math_sense: Dict[str, Set[int]] = {}
        from src.syntax_tree.first_order_logic import CNFFirstOrderLogicFormula
        for element_type in [Variable, Functor, Predicate, Atom, CNFClause, CNFFirstOrderLogicFormula]:
            self._hashes_in_math_sense[element_type.__name__] = set()
            self.info.number_of_instances[element_type.__name__] = 0
            self.info.number_of[element_type.__name__] = 0

    def visit_pre(self, element: CNFFirstOrderLogicFormula):
        super().visit_pre(element)

    def visit_variable_pre(self, element: Variable):
        self._hashes_in_math_sense[Variable.__name__].add(
            MathSense.hash_variable(self.last_visited_cnf_clause, element))
        # todo this should not be computed every visit, only post CNFFormula
        self.info.number_of[Variable.__name__] = len(self._hashes_in_math_sense[Variable.__name__])
        self.info.number_of_instances[Variable.__name__] += 1

    def visit_functor_pre(self, element: Functor):
        self._hashes_in_math_sense[Functor.__name__].add(MathSense.hash_functor(element))
        self.info.number_of_instances[Functor.__name__] += 1
        self.info.number_of[Functor.__name__] = len(self._hashes_in_math_sense[Functor.__name__])
        self.info.functor_arities[element.arity] += 1
        self.info.term_instances_depths[element.recursion_depth] += 1

    def visit_predicate_pre(self, element: Predicate):
        self._hashes_in_math_sense[Predicate.__name__].add(MathSense.hash_predicate(element))
        self.info.number_of[Predicate.__name__] = len(self._hashes_in_math_sense[Predicate.__name__])
        self.info.number_of_instances[Predicate.__name__] += 1
        self.info.predicate_arities[element.arity] += 1

    def visit_atom_pre(self, element: Atom):
        self._hashes_in_math_sense[Atom.__name__].add(MathSense.hash_atom(self.last_visited_cnf_clause, element))
        self.info.number_of[Atom.__name__] = len(self._hashes_in_math_sense[Atom.__name__])
        self.info.number_of_instances[Atom.__name__] += 1
        if element.math_connective and \
                element.math_connective.connective in {MathConnective.EQUAL, MathConnective.NOT_EQUAL}:
            self.info.number_of_equality_atom_instances += 1
        if LogicalConnective.NOT in element.unary_connectives:
            self.info.number_of_negated_literal_instances += 1

    def visit_cnf_clause_pre(self, element: CNFClause):
        self._hashes_in_math_sense[CNFClause.__name__].add(MathSense.hash_clause(element))
        self.info.number_of[CNFClause.__name__] = len(self._hashes_in_math_sense[CNFClause.__name__])
        # variable is clause scoped - this might be TPTP specific
        self.info.number_of_singleton_variables += element.number_of_singleton_variables
        self.info.number_of_instances[CNFClause.__name__] += 1
        self.info.clause_lengths[element.length] += 1
        if element.is_horn:
            self.info.number_of_horn_clauses_instances += 1
        self.last_visited_cnf_clause = element

    def visit_cnf_formula_pre(self, element: CNFFirstOrderLogicFormula):
        from src.syntax_tree.first_order_logic import CNFFirstOrderLogicFormula
        self.info.number_of[CNFFirstOrderLogicFormula.__name__] += 1
        self.info.number_of_instances[CNFFirstOrderLogicFormula.__name__] += 1
        # instances can be handled here (but should they?)
