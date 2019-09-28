from __future__ import annotations

import random
from typing import Dict

from src.ast.fol import CNFFormula, Variable, Functor, CNFClause, Literal, Atom, Predicate
from src.containers.fol import CNFClauseContainer, LiteralContainer, AtomContainer, VariableContainer, FunctorContainer, \
    PredicateContainer


class RandomCNFGenerator:
    def __init__(self, functors: Dict[Functor, float],
                 predicates: Dict[Predicate, float],
                 atoms: Dict[Atom, float],
                 literals: Dict[Literal, float],
                 clauses: Dict[CNFClause, float]):
        self.ast_elements = {
            Functor: functors,
            Predicate: predicates,
            Atom: atoms,
            Literal: literals,
            CNFClause: clauses
        }

    def cnf_formula(self, number_of_clauses: int) -> CNFFormula:
        return CNFFormula(items=self.cnf_clauses(number_of_clauses=number_of_clauses))

    def cnf_clauses(self, number_of_clauses: int) -> CNFClauseContainer:
        return CNFClauseContainer(items=(r.instantiate() for r in
                                         random.choices(population=list(self.ast_elements[CNFClause].keys()),
                                                        weights=list(self.ast_elements[CNFClause].values()),
                                                        k=number_of_clauses)))

    def literals(self, number_of_literals: int) -> LiteralContainer:
        return LiteralContainer(items=(r.instantiate() for r in
                                       random.choices(population=list(self.ast_elements[Literal].keys()),
                                                      weights=list(self.ast_elements[Literal].values()),
                                                      k=number_of_literals)))

    def predicates(self, number_of_predicates: int) -> PredicateContainer:
        return PredicateContainer(items=(r.instantiate() for r in
                                         random.choices(population=list(self.ast_elements[Predicate].keys()),
                                                        weights=list(self.ast_elements[Predicate].values()),
                                                        k=number_of_predicates)))

    def atoms(self, number_of_atoms: int) -> AtomContainer:
        return AtomContainer(items=(r.instantiate() for r in
                                    random.choices(population=list(self.ast_elements[Atom].keys()),
                                                   weights=list(self.ast_elements[Atom].values()),
                                                   k=number_of_atoms)))

    def functors(self, number_of_functors: int) -> FunctorContainer:
        return FunctorContainer(items=(r.instantiate() for r in
                                       random.choices(population=list(self.ast_elements[Functor].keys()),
                                                      weights=list(self.ast_elements[Functor].values()),
                                                      k=number_of_functors)))

    def variables(self, number_of_variables: int) -> VariableContainer:
        return VariableContainer(items=random.choices(
            population=[Variable(name=f'v{i}') for i in range(number_of_variables)],
            k=number_of_variables))

    def recursive_generate(self, ast_element):
        # todo mixed placeholders with ast_elements are not supported
        do_literals = False
        do_atoms = False
        do_predicates = False
        do_functors = False
        do_variables = False
        if isinstance(ast_element, CNFClauseContainer):
            do_literals = True
            do_atoms = True
            do_predicates = True
            do_functors = True
            do_variables = True
        elif isinstance(ast_element, AtomContainer):
            do_literals = False
            do_atoms = True
            do_predicates = True
            do_functors = True
            do_variables = True
        elif isinstance(ast_element, PredicateContainer):
            do_literals = False
            do_atoms = False
            do_predicates = True
            do_functors = True
            do_variables = True
        elif isinstance(ast_element, FunctorContainer):
            do_literals = False
            do_atoms = False
            do_predicates = False
            do_functors = True
            do_variables = True
        elif isinstance(ast_element, VariableContainer):
            do_literals = False
            do_atoms = False
            do_predicates = False
            do_functors = False
            do_variables = True

        if do_literals:
            literal_cont = self.literals(number_of_literals=ast_element.number_of_literal_instances).literals()
            for container, i, literal in ast_element.literals(enum=True):
                item = next(literal_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if do_atoms:
            atom_cont = self.atoms(number_of_atoms=ast_element.number_of_atom_instances).atoms()
            for container, i, atom in ast_element.atoms(enum=True):
                item = next(atom_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if do_predicates:
            pred_cont = self.predicates(number_of_predicates=ast_element.number_of_predicate_instances).predicates()
            for container, i, pred in ast_element.predicates(enum=True):
                item = next(pred_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if do_functors:
            functor_cont = self.functors(number_of_functors=ast_element.number_of_functor_instances).functors()
            for container, i, functor in ast_element.functors(enum=True):
                item = next(functor_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if do_variables:
            variable_cont = self.variables(number_of_variables=ast_element.number_of_variable_instances).variables()
            for container, i, variable in ast_element.variables(enum=True):
                item = next(variable_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()
