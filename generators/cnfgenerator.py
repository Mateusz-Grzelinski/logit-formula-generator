from __future__ import annotations

import random
from typing import Iterable

from ast import CNFFormula, Variable
from ast.containers import CNFClauseContainer, LiteralContainer, AtomContainer, VariableContainer, FunctorContainer
from generators.factories import FunctorFactory, PredicateFactory, AtomFactory, LiteralFactory, CNFClauseFactory
from generators.placeholder import FunctorPlaceholder, PredicatePlaceholder, AtomPlaceholder, LiteralPlaceholder, \
    CNFClausePlaceholder


class GenerationException(Exception):
    repair_policy = None
    problematic_element: AstElement = None
    problematic_attribute: str = None
    min_value: int = None
    max_value: int = None


class CNFGenerator:
    def __init__(self, functors: Iterable[FunctorPlaceholder],
                 predicates: Iterable[PredicatePlaceholder],
                 atoms: Iterable[AtomPlaceholder],
                 literals: Iterable[LiteralPlaceholder],
                 clauses: Iterable[CNFClausePlaceholder],
                 threshold: float = 0.05,
                 max_retries=5):
        self.functors = list(functors)
        self.predicates = list(predicates)
        self.atoms = list(atoms)
        self.literals = list(literals)
        self.clauses = list(clauses)
        self.max_retries = max_retries
        self.threshold = threshold

    def generate_cnf_formula(self,
                             number_of_clauses: int,
                             number_of_atoms: int,
                             number_of_predicates: int,
                             number_of_functors: int,
                             number_of_variables: int,
                             ):
        """
% Syntax   : Number of clauses     :    3 (   0 non-Horn;   3 unit;   1 RR)
%            Number of atoms       :    3 (   3 equality)
%            Maximal clause size   :    1 (   1 average)
%            Number of predicates  :    1 (   0 propositional; 2-2 arity)
%            Number of functors    :    4 (   2 constant; 0-2 arity)
%            Number of variables   :    6 (   0 singleton)
%            Maximal term depth    :    4 (   3 average)
"""
        print(f'{number_of_clauses=}')
        print(f'{number_of_atoms=}')
        print(f'{number_of_predicates=}')
        print(f'{number_of_functors=}')
        print(f'{number_of_variables=}')
        clause_cont = self.generate_cnf_clauses(
            number_of_clauses=number_of_clauses,
        )

        literal_cont = self.generate_literals(
            number_of_literals=clause_cont.number_of_literal_instances,
        )
        for container, i, literal in clause_cont.literals(enum=True):
            container[i] = literal_cont.pop()

        atom_cont = self.generate_atoms(
            number_of_atoms=clause_cont.number_of_atom_instances,
        )
        for container, i, atom in clause_cont.atoms(enum=True):
            container[i] = atom_cont.pop()

        functor_cont = self.generate_functors(
            number_of_functors=clause_cont.number_of_functor_instances,
        )
        for container, i, functor in clause_cont.functors(enum=True, include_nested_items=False):  # todo
            container[i] = functor_cont.pop()

        variable_cont = self.generate_variables(
            number_of_variables=clause_cont.number_of_variable_instances,
        )
        for container, i, variable in clause_cont.variables(enum=True):
            container[i] = variable_cont.pop()

        return CNFFormula(clauses=clause_cont._items)

    def generate_cnf_clauses(self, number_of_clauses: int) -> CNFClauseContainer:
        return CNFClauseContainer(additional_containers=[],
                                  items=random.choices(self.clauses, k=number_of_clauses))

    def generate_literals(self, number_of_literals: int) -> LiteralContainer:
        return LiteralContainer(additional_containers=[],
                                items=random.choices(self.literals, k=number_of_literals))

    def generate_atoms(self, number_of_atoms: int) -> AtomContainer:
        return AtomContainer(additional_containers=[],
                             items=random.choices(self.atoms, k=number_of_atoms))

    def generate_functors(self, number_of_functors: int) -> FunctorContainer:
        return FunctorContainer(additional_containers=[],
                                items=random.choices(self.functors, k=number_of_functors))

    def generate_variables(self, number_of_variables: int) -> VariableContainer:
        return VariableContainer(additional_containers=[],
                                 items=random.choices([Variable(name=f'v{i}') for i in range(number_of_variables)],
                                                      k=number_of_variables))


if __name__ == '__main__':
    g = CNFGenerator(
        functors=FunctorFactory.generate_functors(names=['f'], arities=[0, 1], max_recursion_depth=1),
        predicates=PredicateFactory.generate_predicates(names=['p'], arities=[1, 2]),
        atoms=AtomFactory.generate_atoms({''}),
        literals=LiteralFactory.generate_literals(allow_negated=True),
        clauses=CNFClauseFactory.generate_clauses(lengths=[1, 2, 3, 4]),
        threshold=0.4,
    )

    print(f'{g.functors=}')
    print(f'{g.predicates=}')
    print(f'{g.atoms=}')
    print(f'{g.literals=}')
    print(f'{g.clauses=}')

    formula = g.generate_cnf_formula(
        number_of_clauses=10,
        number_of_atoms=20,
        number_of_predicates=7,
        number_of_functors=5,
        number_of_variables=7
    )
    print(f'\ngenerated formula: {formula}')
