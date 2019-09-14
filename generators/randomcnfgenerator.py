from __future__ import annotations

import random
from typing import Iterable

from ast import CNFFormula, Variable
from ast.containers import CNFClauseContainer, LiteralContainer, AtomContainer, VariableContainer, FunctorContainer, \
    PredicateContainer
from generators import Weight
from generators.placeholder import FunctorPlaceholder, PredicatePlaceholder, AtomPlaceholder, LiteralPlaceholder, \
    CNFClausePlaceholder


class RandomCNFGenerator:
    def __init__(self, functors: Iterable[FunctorPlaceholder],
                 predicates: Iterable[PredicatePlaceholder],
                 atoms: Iterable[AtomPlaceholder],
                 literals: Iterable[LiteralPlaceholder],
                 clauses: Iterable[CNFClausePlaceholder],
                 functor_weights: Iterable[Weight] = None,
                 predicate_weights: Iterable[Weight] = None,
                 atom_weights: Iterable[Weight] = None,
                 literal_weights: Iterable[Weight] = None,
                 clause_weights: Iterable[Weight] = None,
                 ):
        self.functors = list(functors)
        self.predicates = list(predicates)
        self.atoms = list(atoms)
        self.literals = list(literals)
        self.clauses = list(clauses)
        self.functor_weights = list(functor_weights) if functor_weights is not None else None
        self.predicate_weights = list(predicate_weights) if predicate_weights is not None else None
        self.atom_weights = list(atom_weights) if atom_weights is not None else None
        self.literal_weights = list(literal_weights) if literal_weights is not None else None
        self.clause_weights = list(clause_weights) if clause_weights is not None else None

    def generate_cnf_formula(self, number_of_clauses: int) -> CNFFormula:
        """
% Syntax   : Number of clauses     :    3 (   0 non-Horn;   3 unit;   1 RR)
%            Number of atoms       :    3 (   3 equality)
%            Maximal clause size   :    1 (   1 average)
%            Number of predicates  :    1 (   0 propositional; 2-2 arity)
%            Number of functors    :    4 (   2 constant; 0-2 arity)
%            Number of variables   :    6 (   0 singleton)
%            Maximal term depth    :    4 (   3 average)
"""
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

    def generate_cnf_clauses(self, number_of_clauses: int) -> CNFClauseContainer:
        return CNFClauseContainer(additional_containers=[],
                                  items=(r.instantiate() for r in
                                         random.choices(self.clauses, weights=self.clause_weights,
                                                        k=number_of_clauses)))

    def generate_literals(self, number_of_literals: int) -> LiteralContainer:
        return LiteralContainer(additional_containers=[],
                                items=(r.instantiate() for r in
                                       random.choices(self.literals, weights=self.literal_weights,
                                                      k=number_of_literals)))

    def generate_predicates(self, number_of_predicates: int) -> PredicateContainer:
        return PredicateContainer(additional_containers=[],
                                  items=(r.instantiate() for r in
                                         random.choices(self.predicates, weights=self.predicate_weights,
                                                        k=number_of_predicates)))

    def generate_atoms(self, number_of_atoms: int) -> AtomContainer:
        return AtomContainer(additional_containers=[],
                             items=(r.instantiate() for r in
                                    random.choices(self.atoms, weights=self.atom_weights, k=number_of_atoms)))

    def generate_functors(self, number_of_functors: int) -> FunctorContainer:
        return FunctorContainer(additional_containers=[],
                                items=(r.instantiate() for r in
                                       random.choices(self.functors, weights=self.functor_weights,
                                                      k=number_of_functors)))

    def generate_variables(self, number_of_variables: int) -> VariableContainer:
        return VariableContainer(additional_containers=[],
                                 items=random.choices([Variable(name=f'v{i}') for i in range(number_of_variables)],
                                                      k=number_of_variables))
