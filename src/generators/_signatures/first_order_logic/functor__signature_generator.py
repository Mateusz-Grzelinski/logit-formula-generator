from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from itertools import product
from random import sample, shuffle, choice
from typing import Iterable, Dict, Generator, List

from src.ast.first_order_logic import Functor, Variable
from src.generators import AstGenerator
from src.generators._signatures.first_order_logic.variable_name_generator import VariableNameGenerator


class FunctorSignatureGenerator(AstGenerator):
    variable_name = 'V'

    def __init__(self, variable_name_gen: VariableNameGenerator, arities: Iterable[int], functor_names: Iterable[str],
                 max_recursion_depth: int,
                 random: bool = True):
        self.random = random
        self.max_recursion_depth = max_recursion_depth
        self.arities = set(arities)
        self.functor_name_for_arity = {}
        self.variable_name_gen = variable_name_gen
        functor_names = shuffle(list(functor_names)) if not functor_names else [f'f{i}' for i in
                                                                                range(len(self.arities))]
        for arity in arities:
            self.functor_name_for_arity[arity] = [functor_names.pop()]
        while functor_names:
            self.functor_name_for_arity[choice(arities)].append(functor_names.pop())

    def generate(self) -> Generator[Functor, None, None]:
        # first generate non-recursive structures
        functors = set()
        for arity in self.arities:
            functor = Functor(name=choice(self.functor_name_for_arity[arity]),
                              items=[Variable(name=self.variable_name) for i in range(arity)])
            functors.add(functor)

        # now generate nested structures
        for arity in self.arities:
            last_functor_length = None
            while last_functor_length != len(functors):
                last_functor_length = len(functors)
                # Dict[argument_number, argument_candidates]
                terms: Dict[int, List[Term]] = defaultdict(list)
                for argument_index in range(arity):
                    terms[argument_index].append(Variable(self.variable_name))
                    for functor in functors:
                        if functor.recursion_depth >= self.max_recursion_depth:
                            continue
                        terms[argument_index].append(functor)

                    for n_args in product(*terms.values()):
                        functor = Functor(name='f', items=deepcopy(n_args))
                        functors.add(functor)
        functors = sample(functors, len(functors)) if self.random else functors
        for functor in functors:
            if functor.arity in self.arities:
                functor.name = choice(self.functor_name_for_arity[functor.arity])
                for var in functor.items(type=Variable):
                    var.name = self.variable_name_gen.generate()
                yield functor
