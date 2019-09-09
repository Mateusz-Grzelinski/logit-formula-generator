from __future__ import annotations

import itertools
from collections import OrderedDict
from typing import Iterable, Set, List, Dict

from generators.placeholder import PredicatePlaceholder, VariablePlaceholder, TermPlaceholder, FunctorPlaceholder, \
    AtomPlaceholder, LiteralPlaceholder, CNFClausePlaceholder


class FunctorFactory:
    """Factory can not store resursive placeholder"""

    @staticmethod
    def generate_functors(
            names: Iterable[str],
            arities: Iterable[int],
            max_recursion_depth: int,
    ) -> Set[FunctorPlaceholder]:
        var_placeholder = VariablePlaceholder()

        # first generate non-recursive structures
        functors: Set[FunctorPlaceholder] = set()
        for name, arity in itertools.product(names, arities):
            functors.add(FunctorPlaceholder(name=name, terms=[var_placeholder] * arity))

        # now generate nested structures
        for name, arity in itertools.product(names, arities):
            # Dict[argument_number, argument_candidates]
            terms: Dict[int, List[FunctorPlaceholder, VariablePlaceholder]] = OrderedDict()

            last_functor_length = None
            while last_functor_length != len(functors):
                last_functor_length = len(functors)
                for argument_index in range(arity):
                    terms[argument_index] = []
                    terms[argument_index].append(var_placeholder)
                    for f in functors:
                        if f.recursion_depth >= max_recursion_depth:
                            continue
                        terms[argument_index].append(f)

                for n_args in itertools.product(*terms.values()):
                    functors.add(FunctorPlaceholder(name=name, terms=list(n_args)))

        return functors

    def generate_liveness(self) -> Set[Functor]:
        pass

    def generate_safety(self) -> Set[Functor]:
        pass


class PredicateFactory:
    @staticmethod
    def generate_predicates(
            names: Iterable[str],
            arities: Iterable[int]
    ):
        var_placeholder = VariablePlaceholder()
        func_placeholder = FunctorPlaceholder()

        predicates: Set[PredicatePlaceholder] = set()
        for name, arity in itertools.product(names, arities):
            # Dict[argument_index, argument_candidates]
            terms: Dict[int, List[TermPlaceholder]] = OrderedDict()

            for argument_index in range(arity):
                terms[argument_index] = [var_placeholder, func_placeholder]

            for n_args in itertools.product(*terms.values()):
                predicates.add(PredicatePlaceholder(name=name, terms=list(n_args)))

        return predicates


class AtomFactory:
    @staticmethod
    def generate_atoms(operands: Iterable[str]):
        var_placeholder = VariablePlaceholder()
        func_placeholder = FunctorPlaceholder()
        pred_placeholder = PredicatePlaceholder()

        atoms: Set[AtomPlaceholder] = set()
        for connective in operands:
            arguments: Dict[int, List[TermPlaceholder]] = OrderedDict()
            arity = 2 if connective in {'=', '!='} else 1

            for argument_index in range(arity):
                arguments[argument_index] = [var_placeholder, func_placeholder, pred_placeholder]

            for n_args in itertools.product(*arguments.values()):
                atoms.add(AtomPlaceholder(connective=connective, arguments=list(n_args)))

        return atoms


class LiteralFactory:
    @staticmethod
    def generate_literals(allow_negated: bool):
        atom_placeholder = AtomPlaceholder()
        literals = {LiteralPlaceholder(atom=atom_placeholder, negated=False)}
        if allow_negated:
            literals.add(LiteralPlaceholder(atom=atom_placeholder, negated=True))

        return literals


class CNFClauseFactory:
    @staticmethod
    def generate_clauses(lengths: Iterable[int]):
        literal_placeholder = LiteralPlaceholder()

        clauses = set()
        for length in lengths:
            literals = [literal_placeholder] * length
            clauses.add(CNFClausePlaceholder(literals=literals))

        return clauses


if __name__ == '__main__':
    from pprint import pprint

    p = PredicateFactory.generate_predicates(names=['p'], arities=[2])
    pprint(p)
