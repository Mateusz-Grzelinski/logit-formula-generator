from __future__ import annotations

from itertools import combinations_with_replacement, chain
from random import sample, randint
from typing import Iterable, Generator

from src.ast.first_order_logic import Variable, Predicate
from src.generators import AstGenerator

variable = Variable('V')


class PredicateSignatureGenerator(AstGenerator):
    def __init__(self, arities: Iterable[int], functor_gen: FunctorGenerator):
        self.arities = set(arities)
        self.functor_gen = functor_gen

    def generate(self, random: bool = True) -> Generator[Predicate, None, None]:
        global variable
        arities = sample(self.arities, len(self.arities)) if random else self.arities

        def predicate_with_defined_arity(arity: int):
            for args in combinations_with_replacement(chain(self.functor_gen.generate(), [variable]),
                                                      arity):
                yield Predicate(name='p', items=args)

        generators = []
        for arity in arities:
            generators.append(predicate_with_defined_arity(arity))

        while generators:
            index = randint(0, len(generators) - 1)
            try:
                yield next(generators[index])
            except StopIteration:
                del generators[index]
