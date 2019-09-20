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
                 clauses: Iterable[WeightedValue[CNFClausePlaceholder]],
                 ):
        self.functors = {f.value: f.weight for f in functors}
        self.predicates = {p.value: p.weight for p in predicates}
        self.atoms = {a.value: a.weight for a in atoms}
        self.literals = {l.value: l.weight for l in literals}
        self.clauses = {c.value: c.weight for c in clauses}

    def generate_cnf_formula(self, number_of_clauses: int) -> CNFFormula:
        clause_cont = self.generate_cnf_clauses(number_of_clauses=number_of_clauses)

        literal_cont = self.generate_literals(number_of_literals=clause_cont.number_of_literal_instances)
        for container, i, literal in clause_cont.literals(enum=True):
            container[i] = literal_cont.pop()

        atom_cont = self.generate_atoms(number_of_atoms=clause_cont.number_of_atom_instances)
        for container, i, atom in clause_cont.atoms(enum=True):
            container[i] = atom_cont.pop()

        pred_cont = self.generate_predicates(number_of_predicates=clause_cont.number_of_predicate_instances)
        for container, i, pred in clause_cont.predicates(enum=True):
            container[i] = pred_cont.pop()

        functor_cont = self.generate_functors(number_of_functors=clause_cont.number_of_functor_instances)
        for container, i, functor in clause_cont.functors(enum=True):
            container[i] = functor_cont.pop()

        variable_cont = self.generate_variables(number_of_variables=clause_cont.number_of_variable_instances)
        for container, i, variable in clause_cont.variables(enum=True):
            container[i] = variable_cont.pop()

        return CNFFormula(clauses=clause_cont._items)

    def number_of_functors_that_can_be_generated(self, number_of_variables: int, number_of_functors: int) -> int:
        return len(self.functors)

    def generate_cnf_clauses(self, number_of_clauses: int) -> CNFClauseContainer:
        return CNFClauseContainer(additional_containers=[],
                                  items=(r.instantiate() for r in
                                         random.choices(population=list(self.clauses.keys()),
                                                        weights=list(self.clauses.values()),
                                                        k=number_of_clauses)))

    def generate_literals(self, number_of_literals: int) -> LiteralContainer:
        return LiteralContainer(additional_containers=[],
                                items=(r.instantiate() for r in
                                       random.choices(population=list(self.literals.keys()),
                                                      weights=list(self.literals.values()),
                                                      k=number_of_literals)))

    def generate_predicates(self, number_of_predicates: int) -> PredicateContainer:
        return PredicateContainer(additional_containers=[],
                                  items=(r.instantiate() for r in
                                         random.choices(population=list(self.predicates.keys()),
                                                        weights=list(self.predicates.values()),
                                                        k=number_of_predicates)))

    def generate_atoms(self, number_of_atoms: int) -> AtomContainer:
        return AtomContainer(additional_containers=[],
                             items=(r.instantiate() for r in
                                    random.choices(population=list(self.atoms.keys()),
                                                   weights=list(self.atoms.values()),
                                                   k=number_of_atoms)))

    def generate_functors(self, number_of_functors: int) -> FunctorContainer:
        return FunctorContainer(additional_containers=[],
                                items=(r.instantiate() for r in
                                       random.choices(population=list(self.functors.keys()),
                                                      weights=list(self.functors.values()),
                                                      k=number_of_functors)))

    def generate_variables(self, number_of_variables: int) -> VariableContainer:
        return VariableContainer(additional_containers=[],
                                 items=random.choices(
                                     population=[Variable(name=f'v{i}') for i in range(number_of_variables)],
                                     k=number_of_variables))
