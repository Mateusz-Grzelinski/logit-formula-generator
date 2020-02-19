from __future__ import annotations

from collections import defaultdict
from typing import Optional, Dict, Set

from logic_formula_generator.data_model._cnf_fol_formula_info import CNFFOLFormulaInfo
from logic_formula_generator.syntax_tree import MathConnective, LogicalConnective
from logic_formula_generator.syntax_tree.first_order_logic._atom import Atom
from logic_formula_generator.syntax_tree.first_order_logic._fol_formula import FirstOrderLogicFormula
from logic_formula_generator.syntax_tree.first_order_logic._functor import Functor
from logic_formula_generator.syntax_tree.first_order_logic._predicate import Predicate
from logic_formula_generator.syntax_tree.first_order_logic._variable import Variable
from logic_formula_generator.syntax_tree.first_order_logic.visitors.first_order_logic_visitor import FirstOrderLogicSyntaxTreeVisitor


def is_horn(clause) -> bool:
    """A Horn clause is a clause (a disjunction of literals) with at most one positive, i.e. unnegated, literal"""
    from logic_formula_generator.syntax_tree.first_order_logic import Atom
    positive_literals = 0
    for atom in clause:
        atom: Atom
        if LogicalConnective.NOT in atom.unary_connectives:
            positive_literals += 1
    return positive_literals <= 1


def number_of_singleton_variables(clause) -> int:
    from logic_formula_generator.syntax_tree.first_order_logic import Variable
    variables = list(clause.recursive_nodes(type=Variable))
    singleton_vars = set([x for x in variables if variables.count(x) == 1])
    return len(singleton_vars)


class MathSense:
    @staticmethod
    def hash_variable(scope: Optional[FirstOrderLogicFormula], variable: Variable) -> int:
        return hash((id(scope), variable.name))

    @staticmethod
    def hash_functor(functor: Functor) -> int:
        return hash(functor.name) ^ functor.arity

    @staticmethod
    def hash_predicate(predicate: Predicate) -> int:
        return hash((predicate.name, predicate.arity))

    @staticmethod
    def hash_atom(scope: Optional[FirstOrderLogicFormula], atom: Atom) -> int:
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
    def hash_clause(clause: FirstOrderLogicFormula) -> int:
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
        self.last_visited_cnf_clause: Optional[FirstOrderLogicFormula] = None  # or quantifier
        self._hashes_in_math_sense: Dict[str, Set[int]] = {}
        for element_type in ['variables', 'functors', 'predicates', 'atoms', 'clauses']:
            self._hashes_in_math_sense[element_type] = set()
            self.info.number_of_instances[element_type] = 0
            self.info.number_of[element_type] = 0

    def visit_pre(self, element: FirstOrderLogicFormula):
        super().visit_pre(element)

    def visit_variable_pre(self, element: Variable):
        self._hashes_in_math_sense['variables'].add(
            MathSense.hash_variable(self.last_visited_cnf_clause, element))
        # todo this should not be computed every visit, only post CNFFormula
        self.info.number_of['variables'] = len(self._hashes_in_math_sense['variables'])
        self.info.number_of_instances['variables'] += 1

    def visit_functor_pre(self, element: Functor):
        self._hashes_in_math_sense['functors'].add(MathSense.hash_functor(element))
        self.info.number_of_instances['functors'] += 1
        self.info.number_of['functors'] = len(self._hashes_in_math_sense['functors'])
        self.info.functor_arities[element.arity] += 1
        self.info.term_instances_depths[element.recursion_depth] += 1

    def visit_predicate_pre(self, element: Predicate):
        self._hashes_in_math_sense['predicates'].add(MathSense.hash_predicate(element))
        self.info.number_of['predicates'] = len(self._hashes_in_math_sense['predicates'])
        self.info.number_of_instances['predicates'] += 1
        self.info.predicate_arities[element.arity] += 1

    def visit_atom_pre(self, element: Atom):
        self._hashes_in_math_sense['atoms'].add(MathSense.hash_atom(self.last_visited_cnf_clause, element))
        self.info.number_of['atoms'] = len(self._hashes_in_math_sense['atoms'])
        self.info.number_of_instances['atoms'] += 1
        if element.math_connective and \
                element.math_connective.connective in {MathConnective.EQUAL, MathConnective.NOT_EQUAL}:
            self.info.number_of_equality_atom_instances += 1
        if LogicalConnective.NOT in element.unary_connectives:
            self.info.number_of_negated_literal_instances += 1

    def visit_fol_formula_pre(self, element: FirstOrderLogicFormula):
        # def visit_cnf_clause_pre(self, element: FirstOrderLogicFormula):
        if element.logical_connective == LogicalConnective.OR:
            self._hashes_in_math_sense['clauses'].add(MathSense.hash_clause(element))
            self.info.number_of['clauses'] = len(self._hashes_in_math_sense['clauses'])
            # variable is clause scoped - this might be TPTP specific
            # todo
            self.info.number_of_singleton_variables += number_of_singleton_variables(element)
            self.info.number_of_instances['clauses'] += 1
            self.info.clause_lengths[len(element)] += 1
            if is_horn(element):
                self.info.number_of_horn_clauses_instances += 1
            self.last_visited_cnf_clause = element
