from __future__ import annotations

import copy
import itertools
import sys
from dataclasses import dataclass
from statistics import mean
from typing import Tuple, List, Union, Generator, Iterator, Dict, Set, Literal

from src.clause import ClauseGenerator, Clause, KSATClauseGenerator
from src.literal import LiteralPicker, RandomLiteralGenerator


@dataclass
class Mix:
    indexes: Tuple[int, ...]
    number_of_clauses: int = 1
    number_of_literals: int = 1

    @staticmethod
    def chain_mix(clause_groups_length: int, groups_per_mix: int, skip: int = 0) -> List[Mix]:
        """
        :return mixes with indexes set to chain pattern, ex.

        groups_per_mix=2: (0,1), (1,2), (2,3), ...
        groups_per_mix=3: (0,1,2), (1,2,3), ...
        groups_per_mix=3, skip=1: (0,1,2), (2,3,4), ...
        """
        mixes = []

        if skip != 0:
            ran = range(0, clause_groups_length, skip)
        else:
            ran = range(clause_groups_length)

        for i in ran:
            if i + groups_per_mix > clause_groups_length:
                break
            mix = Mix(indexes=tuple(j for j in range(i, i + groups_per_mix)))
            mixes.append(mix)
        return mixes


class Formula:
    def __init__(self, clauses: Union[List[Clause], List[List[Clause]]] = None):
        if all(isinstance(el, list) for el in clauses) and isinstance(clauses, list):
            self.clause_groups = clauses
        elif isinstance(clauses, list):
            self.clause_groups = [clauses]
        else:
            raise Exception('clauses must be list of lists, or list of clauses')

    @property
    def clauses(self) -> Iterator[Clause]:
        return itertools.chain.from_iterable(self.clause_groups)

    def to_tptp(self) -> Generator[None, List[str], None]:
        for clause in self.clauses:
            yield clause.to_tptp()

    @property
    def max_term_depth(self) -> int:
        max_result = 0
        for clause in self.clauses:
            max_result = max(max_result, max(atom.arity for atom in clause.atoms))
            # add functors in furture
            # for atom in clause.atoms:
            #     max_result = max(functor.arity for functor in atom.functors)
        return max_result

    @property
    def atoms(self) -> Set[Atom]:
        atoms = set()
        for clause in self.clauses:
            atoms.update(clause.atoms)
        return atoms

    @property
    def number_of_atoms(self) -> int:
        return len(self.atoms)

    @property
    def total_atoms(self) -> List[Atom]:
        atoms = list()
        for clause in self.clauses:
            atoms.extend(clause.total_atoms)
        return atoms

    @property
    def total_number_of_atoms(self) -> int:
        return len(self.total_atoms)

    @property
    def literals(self) -> Set[Literal]:
        """Deduplicated literals"""
        literals = set()
        for clause in self.clauses:
            literals.update(clause.total_literals)
        return literals

    @property
    def number_of_literals(self) -> int:
        # this logic will become more complex, when equality and recursive term is supported
        return len(self.literals)

    @property
    def total_literals(self) -> List[Literal]:
        """Literals with duplicates"""
        literals = list()
        for clause in self.clauses:
            literals.extend(clause.total_literals)
        return literals

    @property
    def total_number_of_literals(self) -> int:
        return len(self.total_literals)

    @property
    def total_number_of_negated_literals(self) -> int:
        return sum(clause.total_number_of_negated_literals for clause in self.clauses)

    @property
    def number_of_clauses(self) -> int:
        return len(list(self.clauses))

    @property
    def max_clause_size(self) -> int:
        return max(clause.total_number_of_literals for clause in self.clauses)

    @property
    def average_clause_size(self) -> float:
        return mean(clause.total_number_of_literals for clause in self.clauses)

    @property
    def number_of_predicates(self) -> int:
        return sum(clause.number_of_predicates for clause in self.clauses)

    @property
    def number_of_functors(self) -> int:
        """Functor is predicate that returns term. Variables have scope per clause.

        For example: `cnf(p0(A), p1(A)` has 1 variable called `A`
        """
        return sum(clause.number_of_functors for clause in self.clauses)

    @property
    def total_number_of_functors(self) -> int:
        return sum(clause.total_number_of_functors for clause in self.clauses)

    @property
    def number_of_variables(self) -> int:
        """Variable is term that starts with uppercase. Variables have scope per clause.

        For example: `cnf(p0(A), p1(A)` has 1 variable called `A`
        """
        return sum(clause.number_of_variables for clause in self.clauses)

    @property
    def total_number_of_variables(self) -> int:
        """Number of variables, ignoring their scope. This is not a correct way of counting variables.

        For example: `cnf(p0(A), p1(A)` has 2 variables called `A`
        """
        return sum(clause.total_number_of_variables for clause in self.clauses)

    @property
    def number_of_singleton_variables(self) -> int:
        """Singleton variables is used only once in clause

        For example: `cnf(name, axiom, p(A) | p(B) | p(A))` has 1 singleton variable `B`
        """
        return sum(clause.number_of_singleton_variables for clause in self.clauses)

    @property
    def number_of_unit_clauses(self) -> int:
        """Unit clause has only one atom"""
        return len([clause for clause in self.clauses if clause.is_unit])

    @property
    def predicate_arities(self) -> Dict[int, int]:
        """:return dictionary: key is arity, values is number of occurrences"""
        predicates = {}
        for clause in self.clauses:
            for predicate_arity, predicate_occurrences in clause.predicate_arities.items():
                if predicates.get(predicate_arity) is not None:
                    predicates[predicate_arity] += predicate_occurrences
                else:
                    predicates[predicate_arity] = predicate_occurrences
        return predicates

    @property
    def functor_arities(self) -> Dict[int, int]:
        """:return dictionary: key is arity, values is number of occurrences"""
        functors = {}
        for clause in self.clauses:
            for functor_arity, functor_arity_occurrences in clause.functor_arities.items():
                if functors.get(functor_arity) is not None:
                    functors[functor_arity] += functor_arity_occurrences
                else:
                    functors[functor_arity] = functor_arity_occurrences
        return functors


class FormulaGenerator:
    def __init__(self, mixes: List[Mix], clause_generators: List[ClauseGenerator]):
        self.mixes: List[Mix] = mixes
        self.clause_generators = clause_generators

    def generate(self) -> Formula:
        formula = Formula(clauses=[list(clause_gen) for clause_gen in self.clause_generators])
        formula = self._shuffle(formula)
        return formula

    def _shuffle(self, formula: Formula) -> Formula:
        # todo new clause should be different from all others
        for i, mix in enumerate(self.mixes):
            # indexes, number_of_clauses, mix_clause_gen
            groups = [formula.clause_groups[i] for i in mix.indexes]

            # get all literals that appear in above groups
            literals = set()
            for clause in itertools.chain.from_iterable(groups):
                literals = literals.union(clause.literals)
            for literal in literals.copy():
                new_literal = copy.deepcopy(literal)
                new_literal.is_negated = not new_literal.is_negated
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
    from src.atom import SafetyGenerator, LivenessGenerator, Atom

    m = [Mix(indexes=(0, 1),
             number_of_clauses=2,
             number_of_literals=5),
         Mix(indexes=(0, 1),
             number_of_clauses=2,
             number_of_literals=5),
         ]

    lit_gen = RandomLiteralGenerator(total_literals=10,
                                     unique_literals=5,
                                     predicate_generators=[
                                         # ConstantGenerator(predicate_name='constant'),
                                         SafetyGenerator(predicate_name='safety', argument='A'),
                                         # LivenessGenerator(predicate_name='liveness', argument='a')
                                     ])
    lit_gen2 = RandomLiteralGenerator(total_literals=21,
                                      unique_literals=9,
                                      predicate_generators=[
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
