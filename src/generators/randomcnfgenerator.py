from __future__ import annotations

import random
from typing import Dict, Generator

from src.ast.fol import CNFFormula, Variable, Functor, CNFClause, Literal, Atom, Predicate
from src.containers.fol import CNFClauseContainer, AtomContainer, VariableContainer, FunctorContainer, \
    PredicateContainer


class RandomCNFGenerator:
    def __init__(self,
                 variables: Dict[Variable, float],
                 functors: Dict[Functor, float],
                 predicates: Dict[Predicate, float],
                 atoms: Dict[Atom, float],
                 literals: Dict[Literal, float],
                 clauses: Dict[CNFClause, float]):
        self.ast_elements = {
            Variable: variables,
            Functor: functors,
            Predicate: predicates,
            Atom: atoms,
            Literal: literals,
            CNFClause: clauses
        }

    def random_cnf_formula(self, number_of_clauses: int) -> CNFFormula:
        return CNFFormula(items=self.random_cnf_clauses(number_of_clauses=number_of_clauses))

    def random_cnf_clause(self, number_of_literals: int):
        return CNFClause(items=self.random_literals(number_of_literals=number_of_literals))

    def random_cnf_clauses(self, number_of_clauses: int) -> Generator[CNFClause, None, None]:
        return (r.instantiate() for r in random.choices(population=list(self.ast_elements[CNFClause].keys()),
                                                        weights=list(self.ast_elements[CNFClause].values()),
                                                        k=number_of_clauses))

    def random_literals(self, number_of_literals: int) -> Generator[Literal, None, None]:
        return (r.instantiate() for r in random.choices(population=list(self.ast_elements[Literal].keys()),
                                                        weights=list(self.ast_elements[Literal].values()),
                                                        k=number_of_literals))

    def random_predicates(self, number_of_predicates: int) -> Generator[Predicate, None, None]:
        return (r.instantiate() for r in random.choices(population=list(self.ast_elements[Predicate].keys()),
                                                        weights=list(self.ast_elements[Predicate].values()),
                                                        k=number_of_predicates))

    def random_atoms(self, number_of_atoms: int) -> Generator[Atom, None, None]:
        return (r.instantiate() for r in random.choices(population=list(self.ast_elements[Atom].keys()),
                                                        weights=list(self.ast_elements[Atom].values()),
                                                        k=number_of_atoms))

    def random_functors(self, number_of_functors: int) -> Generator[Functor, None, None]:
        return (r.instantiate() for r in random.choices(population=list(self.ast_elements[Functor].keys()),
                                                        weights=list(self.ast_elements[Functor].values()),
                                                        k=number_of_functors))

    def random_variables(self, number_of_variables: int,
                         variable_scope: CNFClause = None) -> Generator[Variable, None, None]:
        if variable_scope:
            variable_population = [var for var, _weight in self.ast_elements[Variable].items() if
                                   var.scope == variable_scope]
            variable_weights = [weight for var, weight in self.ast_elements[Variable].items() if
                                var.scope == variable_scope]
        else:
            variable_population = list(self.ast_elements[Variable].keys())
            variable_weights = list(self.ast_elements[Variable].values())
        return (r for r in random.choices(population=variable_population,
                                          weights=variable_weights,
                                          k=number_of_variables))

    def replace_inner_placeholders(self, ast_element):
        # todo mixed placeholders with ast_elements are not supported
        if isinstance(ast_element, CNFClauseContainer):
            literal_cont = self.random_literals(number_of_literals=ast_element.number_of_literal_instances)
            for container, i, literal in ast_element.literals(enum=True):
                item = next(literal_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if isinstance(ast_element, AtomContainer):
            atom_cont = self.random_atoms(number_of_atoms=ast_element.number_of_atom_instances)
            for container, i, atom in ast_element.atoms(enum=True):
                item = next(atom_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if isinstance(ast_element, PredicateContainer):
            pred_cont = self.random_predicates(number_of_predicates=ast_element.number_of_predicate_instances)
            for container, i, pred in ast_element.predicates(enum=True):
                item = next(pred_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if isinstance(ast_element, FunctorContainer):
            functor_cont = self.random_functors(number_of_functors=ast_element.number_of_functor_instances)
            for container, i, functor in ast_element.functors(enum=True):
                item = next(functor_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()

        if isinstance(ast_element, VariableContainer):
            variable_cont = self.random_variables(number_of_variables=ast_element.number_of_variable_instances)
            for container, i, variable in ast_element.variables(enum=True):
                item = next(variable_cont)
                item.parent = container
                container[i] = item
                container[i].update_scope()
