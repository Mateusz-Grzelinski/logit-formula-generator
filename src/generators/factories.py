from __future__ import annotations

import itertools
from collections import OrderedDict, defaultdict
from typing import Iterable, List, Dict, Tuple, Union, Callable

from src.ast.fol import Functor
from src.placeholders.fol import PredicatePlaceholder, VariablePlaceholder, TermPlaceholder, FunctorPlaceholder, \
    AtomPlaceholder, LiteralPlaceholder, CNFClausePlaceholder


def unify_representation(values: Iterable, default_weight: float) -> List[Tuple, float]:
    unified_values = []
    for value in values:
        if isinstance(value, tuple):
            unified_values.append(value)
        else:
            unified_values.append((value, default_weight))
    return unified_values


class FunctorFactory:
    var_placeholder = VariablePlaceholder()

    @staticmethod
    def generate_functors(names: Iterable[Union[str, Tuple[str, float]]],
                          arities: Iterable[Union[int, Tuple[int, float]]],
                          max_recursion_depth: int,
                          default_weight: float = 1,
                          weight_mix: Callable[[float, float], float] = max
                          ) -> Dict[FunctorPlaceholder, float]:
        names = unify_representation(values=names, default_weight=default_weight)
        arities = unify_representation(values=arities, default_weight=default_weight)

        # first generate non-recursive structures
        functors = dict()
        for (name, name_weight), (arity, arity_weight) in itertools.product(names, arities):
            functor = FunctorPlaceholder(name=name, items=[FunctorFactory.var_placeholder] * arity)
            functors[functor] = weight_mix(name_weight, arity_weight)

        # now generate nested structures
        for (name, name_weight), (arity, arity_weight) in itertools.product(names, arities):
            # Dict[argument_number, argument_candidates]

            last_functor_length = None
            while last_functor_length != len(functors):
                last_functor_length = len(functors)
                terms: Dict[int, List[TermPlaceholder]] = defaultdict(list)
                for argument_index in range(arity):
                    terms[argument_index].append(FunctorFactory.var_placeholder)
                    for functor in functors:
                        if functor.recursion_depth >= max_recursion_depth:
                            continue
                        terms[argument_index].append(functor)

                    for n_args in itertools.product(*terms.values()):
                        functor = FunctorPlaceholder(name=name, items=n_args)
                        functors[functor] = weight_mix(name_weight, arity_weight)
        return functors

    @staticmethod
    def generate_liveness_functors(names: Iterable[Union[str, Tuple[str, float]]],
                                   default_weight: float = 1) -> Dict[FunctorPlaceholder, Any]:
        functors = dict()
        functor_names = unify_representation(values=names, default_weight=default_weight)
        for name, name_weight in functor_names:
            f = FunctorPlaceholder(name=name, items=[FunctorFactory.var_placeholder])
            functors[f] = name_weight
        return functors

    @staticmethod
    def generate_safety_functors(names: Iterable[Union[str, Tuple[str, float]]],
                                 constant_functors: Iterable[Union[Functor, Tuple[Functor, float]]],
                                 default_weight: float = 1,
                                 weight_mix: Callable[[float, float], float] = max
                                 ) -> Dict[FunctorPlaceholder, float]:
        functors = dict()
        functor_names = unify_representation(values=names, default_weight=default_weight)
        constant_functors = unify_representation(values=constant_functors, default_weight=default_weight)
        for (name, name_weight), (functor, functor_weight) in itertools.product(functor_names, constant_functors):
            f = FunctorPlaceholder(name=name, items=[functor])
            functors[f] = weight_mix(name_weight, functor_weight)
        return functors


class PredicateFactory:
    var_placeholder = VariablePlaceholder()
    func_placeholder = FunctorPlaceholder()

    @staticmethod
    def generate_predicates(names: Iterable[Union[str, Tuple[str, float]]],
                            arities: Iterable[Union[int, Tuple[int, float]]],
                            default_weight: float = 1,
                            weight_mix: Callable[[float, float], float] = max
                            ) -> Dict[PredicatePlaceholder, float]:

        names = unify_representation(values=names, default_weight=default_weight)
        arities = unify_representation(values=arities, default_weight=default_weight)

        predicates = dict()
        for (name, name_weight), (arity, arity_weight) in itertools.product(names, arities):
            # Dict[argument_index, argument_candidates]
            terms: Dict[int, List[TermPlaceholder]] = OrderedDict()

            for argument_index in range(arity):
                terms[argument_index] = [PredicateFactory.var_placeholder, PredicateFactory.func_placeholder]

            for n_args in itertools.product(*terms.values()):
                p = PredicatePlaceholder(name=name, items=list(n_args))
                predicates[p] = weight_mix(name_weight, arity_weight)

        return predicates


class AtomFactory:
    var_placeholder = VariablePlaceholder()
    func_placeholder = FunctorPlaceholder()
    pred_placeholder = PredicatePlaceholder()

    @staticmethod
    def generate_atoms(operands: Iterable[str, Tuple[str, float]],
                       default_weights: float = 1) -> Dict[AtomPlaceholder, float]:
        operands = unify_representation(operands, default_weight=default_weights)
        atoms = dict()
        for connective, weight in operands:
            arguments: Dict[int, List[TermPlaceholder]] = OrderedDict()
            arity = 2 if connective in {'=', '!='} else 1

            if arity == 1:
                arguments[0] = [AtomFactory.var_placeholder, AtomFactory.pred_placeholder]
            elif arity == 2:
                for argument_index in range(arity):
                    arguments[argument_index] = [AtomFactory.var_placeholder, AtomFactory.func_placeholder,
                                                 AtomFactory.pred_placeholder]

            for n_args in itertools.product(*arguments.values()):
                a = AtomPlaceholder(connective=connective, items=list(n_args))
                atoms[a] = weight

        return atoms


class LiteralFactory:
    atom_placeholder = AtomPlaceholder()

    @staticmethod
    def generate_literals(allow_positive: Union[bool, Tuple[bool, float]] = True,
                          allow_negated: Union[bool, Tuple[bool, float]] = True,
                          default_weight: float = 1) -> Dict[LiteralPlaceholder, Union[float]]:
        literals = dict()
        positive_literal = LiteralPlaceholder(item=LiteralFactory.atom_placeholder, negated=False)
        if isinstance(allow_positive, tuple) and allow_positive[0]:
            literals[positive_literal] = allow_positive[1]
        elif isinstance(allow_positive, bool) and allow_positive:
            literals[positive_literal] = default_weight

        negative_literal = LiteralPlaceholder(item=LiteralFactory.atom_placeholder, negated=True)
        if isinstance(allow_negated, tuple) and allow_positive[0]:
            literals[negative_literal] = allow_negated[1]
        elif isinstance(allow_negated, bool) and allow_negated:
            literals[negative_literal] = default_weight
        return literals


class CNFClauseFactory:
    literal_placeholder = LiteralPlaceholder()

    @staticmethod
    def generate_clauses(lengths: Iterable[int, Tuple[int, float]],
                         default_weight: float = 1) -> Dict[CNFClausePlaceholder, float]:
        lengths = unify_representation(lengths, default_weight)
        clauses = dict()
        for length, weight in lengths:
            literals = [CNFClauseFactory.literal_placeholder] * length
            clauses[CNFClausePlaceholder(items=literals)] = weight
        return clauses


if __name__ == '__main__':
    f = FunctorFactory.generate_functors(names=['f'], arities=[1, 2], max_recursion_depth=1)
    fl = FunctorFactory.generate_liveness_functors(names=['fl', 'fll'])
    fs = FunctorFactory.generate_safety_functors(names=['fs', 'fss'], constant_functors={Functor('f2'), Functor('f1')})
    print(f)
    print(fl)
    print(fs)
    # WeightedValue[int]
    # w1 = WeightedValue(Functor('f'), 1.0)
    # w2 = WeightedValue(Functor('f'), 2.0)
    # w3 = WeightedValue(Functor('f2'), 1.0)
    # for f in {w1, w2, w3}:
    #     print(f.value)
