from __future__ import annotations

from collections import defaultdict
from itertools import product
from typing import Iterable, Dict, Generator, List

from src.ast.first_order_logic import Functor, Variable

variable = Variable('V')


class FunctorSignatureGenerator:
    def __init__(self, arities: Iterable[int], max_recursion_depth: int):
        self.max_recursion_depth = max_recursion_depth
        self.arities = set(arities)

    def generate(self) -> Generator[Functor, None, None]:
        global variable

        # first generate non-recursive structures
        functors = set()
        for arity in self.arities:
            functor = Functor(name='f', items=[variable] * arity)
            functors.add(functor)

        # now generate nested structures
        for arity in self.arities:
            last_functor_length = None
            while last_functor_length != len(functors):
                last_functor_length = len(functors)
                # Dict[argument_number, argument_candidates]
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
            if functor.arity in self.arities:
                yield functor
