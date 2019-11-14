from __future__ import annotations

from itertools import product
from random import sample, randint
from typing import Iterable, Generator

from src.ast.first_order_logic import Variable, Predicate
from src.generators import AstGenerator
from src.generators._signatures.first_order_logic import FunctorSignatureGenerator
from src.generators.utils._lazy_itertools import random_chain


class PredicateSignatureGenerator(AstGenerator):
    variable_name = 'V'
    predicate_name = 'p'

    def __init__(self, arities: Iterable[int], functor_gen: FunctorSignatureGenerator, random: bool = True):
        self.random = random
        self.arities = set(arities)
        self.functor_gen = functor_gen

    def generate(self) -> Generator[Predicate, None, None]:
        def predicate_with_defined_arity(arity: int):
            possible_arguments = [random_chain(self.functor_gen.generate(), Variable(name=self.variable_name)) for _ in
                                  range(arity)]
            for args in product(*possible_arguments):
                yield Predicate(name=self.predicate_name, items=args)

        arities = sample(self.arities, len(self.arities)) if self.random else self.arities
        generators = []
        for arity in arities:
            generators.append(predicate_with_defined_arity(arity))

        while generators:
            index = randint(0, len(generators) - 1)
            try:
                yield next(generators[index])
            except StopIteration:
                del generators[index]
