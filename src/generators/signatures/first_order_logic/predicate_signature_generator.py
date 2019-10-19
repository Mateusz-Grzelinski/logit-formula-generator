from __future__ import annotations

from itertools import combinations_with_replacement, chain
from typing import Iterable, Generator

from src.ast.first_order_logic import Variable, Predicate

variable = Variable('V')


class PredicateSignatureGenerator:
    def __init__(self, arities: Iterable[int], functor_gen: FunctorGenerator):
        self.arities = set(arities)
        self.functor_gen = functor_gen

    def generate(self) -> Generator[Predicate, None, None]:
        global variable
        for arity in self.arities:
            for args in combinations_with_replacement(chain(self.functor_gen.generate(), [variable]),
                                                      arity):
                yield Predicate(name='p', items=args)
