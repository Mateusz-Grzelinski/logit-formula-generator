from __future__ import annotations

from random import sample, randint, choice, shuffle
from typing import Iterable, Generator

from src.ast.first_order_logic import Variable, Predicate
from src.generators import AstGenerator
from src.generators._signatures.first_order_logic import FunctorSignatureGenerator
from src.generators._signatures.first_order_logic.variable_name_generator import VariableNameGenerator
from src.generators.utils._lazy_itertools import random_chain, random_lazy_product


class PredicateSignatureGenerator(AstGenerator):
    # variable_name = 'V'
    # predicate_name = 'p'

    def __init__(self, variable_name_gen: VariableNameGenerator, arities: Iterable[int], predicate_names: Iterable[str],
                 functor_gen: FunctorSignatureGenerator, random: bool = True):
        self.variable_gen = variable_name_gen
        self.random = random
        self.arities = set(arities)
        self.predicate_name_for_arity = {}
        predicate_names = shuffle(list(predicate_names)) if not predicate_names else [f'p{i}' for i in
                                                                                      range(len(self.arities))]
        for arity in arities:
            self.predicate_name_for_arity[arity] = [predicate_names.pop()]
        while predicate_names:
            self.predicate_name_for_arity[choice(arities)].append(predicate_names.pop())
        self.functor_gen = functor_gen

    def generate(self) -> Generator[Predicate, None, None]:
        def predicate_with_defined_arity(arity: int):
            possible_arguments = [random_chain(self.functor_gen.generate(), Variable(name=self.variable_gen.generate()))
                                  for _ in
                                  range(arity)]
            for args in random_lazy_product(*possible_arguments):
                yield Predicate(name=choice(self.predicate_name_for_arity[arity]), items=args)

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
