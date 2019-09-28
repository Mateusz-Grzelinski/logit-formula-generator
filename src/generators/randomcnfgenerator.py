from __future__ import annotations

import random
from typing import Iterable

from src.ast import CNFFormula, Variable
from src.ast.containers import CNFClauseContainer, LiteralContainer, AtomContainer, VariableContainer, FunctorContainer, \
    PredicateContainer
from src.generators import WeightedValue
from src.generators.placeholder import FunctorPlaceholder, PredicatePlaceholder, AtomPlaceholder, LiteralPlaceholder, \
    CNFClausePlaceholder


class RandomCNFGenerator:
    def __init__(self, functors: Iterable[WeightedValue[FunctorPlaceholder]],
                 predicates: Iterable[WeightedValue[PredicatePlaceholder]],
                 atoms: Iterable[WeightedValue[AtomPlaceholder]],
                 literals: Iterable[WeightedValue[LiteralPlaceholder]],
                 clauses: Iterable[WeightedValue[CNFClausePlaceholder]]):
        self.functor_placeholders = {f.value: f.weight for f in functors}
        self.predicates_placeholders = {p.value: p.weight for p in predicates}
        self.atom_placeholders = {a.value: a.weight for a in atoms}
        self.literal_placeholders = {l.value: l.weight for l in literals}
        self.clause_placeholders = {c.value: c.weight for c in clauses}

    def cnf_formula(self, number_of_clauses: int) -> CNFFormula:
        return CNFFormula(items=self.cnf_clauses(number_of_clauses=number_of_clauses))

    def cnf_clauses(self, number_of_clauses: int) -> CNFClauseContainer:
        return CNFClauseContainer(additional_containers=[],
                                  items=(r.instantiate() for r in
                                         random.choices(population=list(self.clause_placeholders.keys()),
                                                        weights=list(self.clause_placeholders.values()),
                                                        k=number_of_clauses)))

    def literals(self, number_of_literals: int) -> LiteralContainer:
        return LiteralContainer(additional_containers=[],
                                items=(r.instantiate() for r in
                                       random.choices(population=list(self.literal_placeholders.keys()),
                                                      weights=list(self.literal_placeholders.values()),
                                                      k=number_of_literals)))

    def predicates(self, number_of_predicates: int) -> PredicateContainer:
        return PredicateContainer(additional_containers=[],
                                  items=(r.instantiate() for r in
                                         random.choices(population=list(self.predicates_placeholders.keys()),
                                                        weights=list(self.predicates_placeholders.values()),
                                                        k=number_of_predicates)))

    def atoms(self, number_of_atoms: int) -> AtomContainer:
        return AtomContainer(additional_containers=[],
                             items=(r.instantiate() for r in
                                    random.choices(population=list(self.atom_placeholders.keys()),
                                                   weights=list(self.atom_placeholders.values()),
                                                   k=number_of_atoms)))

    def functors(self, number_of_functors: int) -> FunctorContainer:
        return FunctorContainer(additional_containers=[],
                                items=(r.instantiate() for r in
                                       random.choices(population=list(self.functor_placeholders.keys()),
                                                      weights=list(self.functor_placeholders.values()),
                                                      k=number_of_functors)))

    def variables(self, number_of_variables: int) -> VariableContainer:
        return VariableContainer(additional_containers=[],
                                 items=random.choices(
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
                container[i] = next(literal_cont)

        if do_atoms:
            atom_cont = self.atoms(number_of_atoms=ast_element.number_of_atom_instances).atoms()
            for container, i, atom in ast_element.atoms(enum=True):
                container[i] = next(atom_cont)

        if do_predicates:
            pred_cont = self.predicates(number_of_predicates=ast_element.number_of_predicate_instances).predicates()
            for container, i, pred in ast_element.predicates(enum=True):
                container[i] = next(pred_cont)

        if do_functors:
            functor_cont = self.functors(number_of_functors=ast_element.number_of_functor_instances).functors()
            for container, i, functor in ast_element.functors(enum=True):
                container[i] = next(functor_cont)

        if do_variables:
            variable_cont = self.variables(number_of_variables=ast_element.number_of_variable_instances).variables()
            for container, i, variable in ast_element.variables(enum=True):
                container[i] = next(variable_cont)
