from __future__ import annotations

from collections import defaultdict
from itertools import combinations, combinations_with_replacement, product, chain
from typing import Iterable, Dict, Generator, List, Set

from src.ast.first_order_logic import *


class FunctorGen:
    def __init__(self, arities: Iterable[int], max_recursion_depth: int):
        self.max_recursion_depth = max_recursion_depth
        self.arities = set(arities)

    def generate(self) -> Generator[Functor, None, None]:
        variable = Variable('X')

        # first generate non-recursive structures
        functors = set()
        for arity in range(max(self.arities)):
            functor = Functor(name='f', items=[variable] * arity)
            functors.add(functor)

        # now generate nested structures
        for arity in self.arities:
            # Dict[argument_number, argument_candidates]

            last_functor_length = None
            while last_functor_length != len(functors):
                last_functor_length = len(functors)
                terms: Dict[int, List[Term]] = defaultdict(list)
                for argument_index in range(arity):
                    terms[argument_index].append(variable)
                    for functor in functors:
                        if functor.recursion_depth >= self.max_recursion_depth:
                            continue
                        terms[argument_index].append(functor)

                    for n_args in product(*terms.values()):
                        functor = Functor(name='f', items=n_args)
                        functors.add(functor)
        for functor in functors:
            yield functor


class PredicateGen:
    def generate(self) -> Generator[Predicate, None, None]:
        pass


class AtomGen:
    connective_arities = {'': 1, '=': 2, '!=': 2}
    connective_commutative = {'': True, '=': True, '!=': True}

    def __init__(self, allowed_connectives: Set[str], predicate_gen: PredicateGen):
        self.predicate_gen = predicate_gen
        self.allowed_connectives = allowed_connectives

    def generate(self) -> Generator[Atom, None, None]:
        variable = Variable('A')
        allowed_predicate = self.predicate_gen.generate()
        allowed_atom_items = chain(allowed_predicate, [variable])

        for connective in self.allowed_connectives:
            arity = AtomGen.connective_arities[connective]
            commutative = AtomGen.connective_commutative[connective]
            if commutative:
                for items in combinations(allowed_atom_items, arity):
                    yield Atom(items=items, connective=connective)
            else:
                for items in combinations_with_replacement(allowed_atom_items, arity):
                    yield Atom(items=items, connective=connective)


class LiteralGen:
    def __init__(self, allow_positive: bool, allow_negated: bool, atom_gen: AtomGen):
        self.atom_gen = atom_gen
        self.allow_positive = allow_positive
        self.allow_negated = allow_negated

    def generate(self):
        assert self.allow_positive or self.allow_negated
        for allowed_atom in self.atom_gen.generate():
            if self.allow_negated:
                yield Literal(item=allowed_atom, negated=True)
            if self.allow_positive:
                yield Literal(item=allowed_atom, negated=False)


class CNFClauseGen:
    def __init__(self, literal_gen: LiteralGen):
        self.literal_gen = literal_gen

    def generate(self, clause_length: int) -> Generator[CNFClause, None, None]:
        for argument_position in range(clause_length):
            allowed_literals = self.literal_gen.generate()
            for n_args in combinations(allowed_literals, clause_length):
                yield CNFClause(items=n_args)


if __name__ == '__main__':
    # f = FunctorGen([1, 2], 1).generate()
    # pprint(list(f))

    f1 = Functor('f', items=[Variable('V')])
    f2 = Functor('f', items=[Variable('X')])
    f = {f1, f2, }
    print(f)
