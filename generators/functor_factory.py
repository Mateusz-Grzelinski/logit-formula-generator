import itertools
from collections import OrderedDict
from typing import Iterable, Set, List, Dict

from ast import Functor


class VariablePlaceholder:
    def __str__(self):
        return 'var'


class FunctorFactory:
    @staticmethod
    def generate_functors(
            names: Iterable[str],
            arities: Iterable[int],
            max_recursion_depth: int,
    ):
        var_placeholder = VariablePlaceholder()
        # first generate non-recursive structures
        functors: Set[Functor] = set()
        for name, arity in itertools.product(names, arities):
            functors.add(Functor(name=name, terms=[var_placeholder] * arity))

        # now generate nested structures
        for name, arity in itertools.product(names, arities):
            terms: Dict[int, List[Functor, VariablePlaceholder]] = OrderedDict()

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
                    functors.add(Functor(name=name, terms=list(n_args)))

        return functors

    def generate_liveness(self):
        pass

    def generate_safety(self):
        pass


if __name__ == '__main__':
    f = FunctorFactory.generate_functors(
        names=['f'],
        arities=[1],
        max_recursion_depth=1
    )
    from pprint import pprint

    pprint(f)
    print(len(f))
