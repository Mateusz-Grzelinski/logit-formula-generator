from __future__ import annotations

import copy
import itertools
from dataclasses import dataclass
from typing import Tuple, List

from src.clause import ClauseGenerator, Clause, KSATClauseGenerator
from src.literal import LiteralPicker, RandomLiteralGenerator


@dataclass
class Mix:
    indexes: Tuple[int, ...]
    number_of_clauses: int
    number_of_literals: int

    @staticmethod
    def chain_mix(clause_groups: List[Clause], groups_per_mix: int, skip: int = 0) -> List[Mix]:
        pass


@dataclass
class Formula:
    clause_groups: List[List[Clause]]

    def to_tptp(self):
        out = ''
        for clause in itertools.chain.from_iterable(self.clause_groups):
            out += clause.to_tptp() + '\n'
        return out


class FormulaGenerator:
    def __init__(self, mixes: List[Mix], clause_generators: List[ClauseGenerator]):
        # self.patterns?
        self.mixes: List[Mix] = mixes
        self.clause_generators = clause_generators

    def generate(self):
        f = Formula(clause_groups=[list(clause_gen) for clause_gen in self.clause_generators])
        f = self._shuffle(f)
        return f

    def _shuffle(self, formula: Formula):
        for mix in self.mixes:
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
                print(f"Mix is not possible, skipping {mix}")
            else:
                # print("mix ok")
                clauses = list(clause_gen)
                formula.clause_groups.append(clauses)
        return formula


if __name__ == '__main__':
    m = [Mix(indexes=(0, 1),
             number_of_clauses=2,
             number_of_literals=5),
         Mix(indexes=(0, 1),
             number_of_clauses=2,
             number_of_literals=5),
         ]

    lit_gen = RandomLiteralGenerator(total_literals=10,
                                     unique_literals=5,
                                     name='a')
    clause_gen1 = KSATClauseGenerator(k_clauses={2: 5},
                                      literal_gen=lit_gen)
    clause_gen2 = KSATClauseGenerator(k_clauses={3: 7})
    # cl = list(clause_gen1)
    # for c in cl:
    #     if not c.literals:
    #         print("none!!!!")
    # print([c.to_tptp() for c in cl])
    f = FormulaGenerator(m, clause_generators=[clause_gen1, clause_gen2])
    formula = f.generate()
    print(formula.to_tptp())
