from __future__ import annotations

import copy
import itertools
import sys
from dataclasses import dataclass
from typing import Tuple, List, Union, Iterable, Generator

from src.clause import ClauseGenerator, Clause, KSATClauseGenerator
from src.literal import LiteralPicker, RandomLiteralGenerator


@dataclass
class Mix:
    indexes: Tuple[int, ...]
    number_of_clauses: int
    number_of_literals: int

    @staticmethod
    def chain_mix(clause_groups: List[Clause], groups_per_mix: int, skip: int = 0) -> List[Mix]:
        raise NotImplemented


class Formula:
    def __init__(self, clauses: Union[List[Clause], List[List[Clause]]] = None):
        if all(isinstance(el, list) for el in clauses) and isinstance(clauses, list):
            self.clause_groups = clauses
        elif isinstance(clauses, list):
            self.clause_groups = [clauses]
        else:
            raise Exception('clauses must be list of lists, or list of clauses')

    @property
    def clauses(self) -> Iterable[Clause]:
        return itertools.chain.from_iterable(self.clause_groups)

    def to_tptp(self) -> Generator[None, List[Clause], None]:
        for clause in self.clauses:
            yield clause.to_tptp()

    @property
    def number_of_clauses(self):
        return len(list(self.clauses))

    @property
    def number_of_atoms(self):
        # this logic will become more complex, when equality and recursive term is supported
        return sum(len(clause.literals) for clause in self.clauses)

    @property
    def max_clause_size(self):
        return max(len(clause.literals) for clause in self.clauses)

    @property
    def number_of_predicates(self):
        predicates = set()
        for clause in self.clauses:
            predicates.update(literal.predicate.name for literal in clause.literals)
        return len(predicates)

    @property
    def number_of_functors(self):
        # in general, functor is predicate inside predicate, special case is 0-arity predicate, called constant
        # ex. pred(constant, functor_1(a), functor_2(a, a))
        # see tptp SYN005-1.010.p for reference
        number_of_constants = 0
        for clause in self.clauses:
            variables = set()
            for literal in clause.literals:
                arguments = literal.predicate.arguments
                variables.update(arg for arg in arguments if arg[0].islower())
            number_of_constants += len(variables)
        return number_of_constants

    @property
    def number_of_variables(self):
        # see tptp SYN002-1.007.008.p for reference
        number_of_variables = 0
        for clause in self.clauses:
            variables = set()
            for literal in clause.literals:
                arguments = literal.predicate.arguments
                variables.update(arg for arg in arguments if arg[0].isupper())
            number_of_variables += len(variables)
        return number_of_variables

    @property
    def max_term_depth(self):
        return 1

    @property
    def number_of_negated_literals(self):
        negated_literals = 0
        for clause in self.clauses:
            negated_literals += len([literal for literal in clause.literals if literal.is_negated])
        return negated_literals


class FormulaGenerator:
    def __init__(self, mixes: List[Mix], clause_generators: List[ClauseGenerator]):
        self.mixes: List[Mix] = mixes
        self.clause_generators = clause_generators

    def generate(self) -> Formula:
        formula = Formula(clauses=[list(clause_gen) for clause_gen in self.clause_generators])
        formula = self._shuffle(formula)
        return formula

    def _shuffle(self, formula: Formula) -> Formula:
        for i, mix in enumerate(self.mixes):
            # indexes, number_of_clauses, mix_clause_gen
            groups = [formula.clause_groups[i] for i in mix.indexes]

            # get all literals that appear in above groups
            literals = set()
            for clause in itertools.chain.from_iterable(groups):
                literals = literals.union(clause.literals)
            for literal in literals.copy():
                new_literal = copy.deepcopy(literal)
                new_literal.negated = not new_literal.negated
                literals.add(new_literal)

            try:
                literal_gen = LiteralPicker(literals=list(literals),
                                            total_literals=mix.number_of_literals)
                clause_gen = KSATClauseGenerator(k_clauses='random',
                                                 total_clauses=mix.number_of_clauses,
                                                 literal_gen=literal_gen)
            except Exception as e:
                print(f"Mix is not possible, skipping {mix}", file=sys.stderr)
            else:
                # print("mix ok")
                clauses = list(clause_gen)
                str_indexes = '_'.join(str(i) for i in mix.indexes)
                for clause in clauses:
                    clause.name = f'mix_clause{i}_{str_indexes}'
                formula.clause_groups.append(clauses)
        return formula


if __name__ == '__main__':
    from src.predicate import SafetyGenerator, LivenessGenerator

    m = [Mix(indexes=(0, 1),
             number_of_clauses=2,
             number_of_literals=5),
         Mix(indexes=(0, 1),
             number_of_clauses=2,
             number_of_literals=5),
         ]

    lit_gen = RandomLiteralGenerator(total_literals=10,
                                     unique_literals=5,
                                     predicate_generator=[
                                         # ConstantGenerator(predicate_name='constant'),
                                         SafetyGenerator(predicate_name='safety', argument='A'),
                                         # LivenessGenerator(predicate_name='liveness', argument='a')
                                     ])
    lit_gen2 = RandomLiteralGenerator(total_literals=21,
                                      unique_literals=9,
                                      predicate_generator=[
                                          # ConstantGenerator(predicate_name='constant'),
                                          # SafetyGenerator(predicate_name='safety', argument='A'),
                                          LivenessGenerator(predicate_name='liveness', argument='a')
                                      ])
    clause_gen1 = KSATClauseGenerator(k_clauses={2: 5},
                                      literal_gen=lit_gen)
    clause_gen2 = KSATClauseGenerator(k_clauses={3: 7},
                                      literal_gen=lit_gen2)
    f = FormulaGenerator(mixes=m,
                         clause_generators=[clause_gen1, clause_gen2])
    formula = f.generate()
    print(formula.to_tptp())
