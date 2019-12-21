from __future__ import annotations

import random
from collections import defaultdict
from copy import deepcopy
from itertools import product
from typing import Iterable, Dict, Generator, List

from src.ast.first_order_logic import Functor, Variable
from src.generators import AstGenerator
from .variable_generator import VariableGenerator


class FunctorGenerator(AstGenerator):

    def __init__(self, variable_gen: VariableGenerator, arities: Iterable[int], functor_names: Iterable[str],
                 max_recursion_depth: int):
        self.max_recursion_depth = max_recursion_depth
        self.arities = list(set(arities))
        self.variable_gen = variable_gen
        # it is hard to generate functors on the fly because they are recursive
        self.functors = list(self._pregenerate_functors())
        # one functor name can be assigned to only one arity
        functor_names = list(functor_names)
        assert len(functor_names) >= len(self.arities), \
            f'there must be at least {len(self.arities)} functor names available'
        random.shuffle(functor_names)
        self.functor_name_for_arity = {}
        for arity in self.arities:
            self.functor_name_for_arity[arity] = [functor_names.pop()]
        while functor_names:
            self.functor_name_for_arity[random.choice(self.arities)].append(functor_names.pop())

    def _pregenerate_functors(self) -> Generator[Functor, None, None]:
        variable_initial_name = 'V'
        functor_initial_name = 'f'
        # first generate non-recursive structures
        functors = set()
        for arity in self.arities:
            functor = Functor(name=functor_initial_name,
                              items=[Variable(name=variable_initial_name) for i in range(arity)])
            functors.add(functor)

        # now generate nested structures
        for arity in self.arities:
            last_functor_length = None
            while last_functor_length != len(functors):
                last_functor_length = len(functors)
                # Dict[argument_number, argument_candidates]
                terms: Dict[int, List[Term]] = defaultdict(list)
                for argument_index in range(arity):
                    terms[argument_index].append(Variable(name=variable_initial_name))
                    for functor in functors:
                        if functor.recursion_depth >= self.max_recursion_depth:
                            continue
                        terms[argument_index].append(functor)

                    for n_args in product(*terms.values()):
                        functor = Functor(name=functor_initial_name, items=deepcopy(n_args))
                        functors.add(functor)
        for functor in functors:
            if functor.arity in self.arities:
                yield functor

    def generate(self) -> Functor:
        functor = deepcopy(random.choice(self.functors))
        functor.name = random.choice(self.functor_name_for_arity[functor.arity])
        for var in functor.items(type=Variable):
            var.name = random.choice(self.variable_gen.variable_names)
        return functor
