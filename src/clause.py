import copy
import random
from abc import abstractmethod
from dataclasses import dataclass, field
from math import ceil
from typing import Dict, Set, Union, List

from src.atom import Atom
from src.literal import Literal, LiteralGenerator, RandomLiteralGenerator


@dataclass
class Clause:
    name: str = 'clause_name'
    total_literals: Set[Literal] = field(default_factory=set)

    def to_tptp(self) -> str:
        literal_tptp = (literal.to_tptp() for literal in self.total_literals)
        return f'cnf({self.name}, axiom, ({" | ".join(literal_tptp)}) ).'

    def __hash__(self) -> int:
        return hash(i for i in self.total_literals)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.total_literals == other.total_literals

    @property
    def predicates(self) -> Set[Atom]:
        """:return set of unique predicates in clause"""
        # predicate hash is generated based on name and arguments
        # in maths predicate is unique only based on its name
        # if we would put atoms in set, 2 atoms with the same name and different argument could show up
        predicates = set()
        predicate_names = set()
        for literal in self.total_literals:
            if literal.atom.name not in predicate_names:
                predicates.add(literal.atom)
            predicate_names.add(literal.atom.name)
        return predicates

    @property
    def number_of_predicates(self) -> int:
        """:return number of unique predicates in clause"""
        return len(self.predicates)

    @property
    def total_predicates(self):
        """Like self.predicates, but no deduplication is done"""
        predicates = list()
        for literal in self.total_literals:
            predicates.extend(literal.atom)
        return predicates

    @property
    def total_number_of_predicates(self):
        return len(self.total_predicates)

    @property
    def predicate_arities(self) -> Dict[int, int]:
        predicates = {}
        for pred in self.predicates:
            if predicates.get(pred.arity) is None:
                predicates[pred.arity] = 0
            else:
                predicates[pred.arity] += 1
        return predicates

    @property
    def functors(self) -> Set[str]:
        functors = set()
        for literal in self.total_literals:
            functors.update(literal.atom.functors)
        return functors

    @property
    def number_of_functors(self):
        return len(self.functors)

    @property
    def total_functors(self) -> List[str]:
        total_functors = list()
        for literal in self.total_literals:
            total_functors.extend(literal.atom.total_functors)
        return total_functors

    @property
    def total_number_of_functors(self):
        return len(self.total_functors)

    @property
    def functor_arities(self) -> Dict[int, int]:
        """Not supported. Functor arity is always 0 """
        functors = {}
        for functor in self.total_functors:
            if functors.get(functor) is None:
                # in future: functors[functor.arity] = 0
                functors[0] = 0
            else:
                functors[0] += 1
        return functors

    @property
    def atoms(self):
        """Iterate atoms in clause, without duplicates"""
        atoms = set()
        for literal in self.total_literals:
            atoms.add(literal.atom)
        return atoms

    @property
    def number_of_atoms(self):
        """Similar to self.number_of_literals, but ignores sing.

        if self.number_of_atoms < self.number_of_literals that means in formula there is used atom and `not` atom
        """
        return len(self.atoms)

    @property
    def total_atoms(self):
        """Atoms with duplicates"""
        atoms = list()
        for literal in self.total_literals:
            atoms.append(literal.atom)
        return atoms

    @property
    def total_number_of_atoms(self):
        return len(self.total_atoms)

    @property
    def total_number_of_literals(self) -> int:
        return len(self.total_literals)

    @property
    def total_number_of_negated_literals(self) -> int:
        return len([literal for literal in self.total_literals if literal.is_negated])

    @property
    def is_unit(self) -> bool:
        """Unit clause is clause with one predicate"""
        return len(self.predicates) == 1

    @property
    def variables(self) -> Set[str]:
        variables = set()
        for literal in self.total_literals:
            variables.update(literal.atom.variables)
        return variables

    @property
    def number_of_variables(self) -> int:
        return len(self.variables)

    @property
    def total_variables(self) -> List[str]:
        variables = list()
        for literal in self.total_literals:
            variables.extend(literal.atom.total_variables)
        return variables

    @property
    def total_number_of_variables(self) -> int:
        return len(self.total_variables)

    @property
    def singleton_variables(self) -> Set[str]:
        repeated_variables = set()
        singleton_variables = set()
        for literal in self.total_literals:
            for variable in literal.atom.variables:
                if variable in repeated_variables:
                    continue

                if variable in singleton_variables:
                    singleton_variables.remove(variable)
                    repeated_variables.add(variable)
                    continue

                singleton_variables.add(variable)
        return singleton_variables

    @property
    def number_of_singleton_variables(self) -> int:
        return len(self.singleton_variables)


class ClauseGenerator:
    @property
    @abstractmethod
    def total_clauses(self) -> int:
        """:return total number of clauses that generator can produce"""

    @property
    def clauses_left(self) -> int:
        """:return number of clauses that generator can still produce"""
        return self.total_clauses - self.generated_clauses

    @property
    @abstractmethod
    def generated_clauses(self) -> int:
        """:return number of clauses that generator has produced"""

    @property
    @abstractmethod
    def clause(self) -> Clause:
        """Generate new clause"""

    def __iter__(self):
        while True:
            if self.clauses_left != 0:
                yield self.clause
            else:
                break


class KSATClauseGenerator(ClauseGenerator):
    """Generate clauses in k-SAT format"""

    def __init__(self, k_clauses: Union[Dict[int, int], str], literal_gen: LiteralGenerator = None,
                 total_clauses: int = None, max_clause_size: int = None):
        self._generated_clauses = set()

        if isinstance(k_clauses, dict):
            self.__exact_constructor(k_clauses=k_clauses,
                                     literal_gen=literal_gen)
        elif k_clauses == 'random':
            self.__random_constructor(literal_gen=literal_gen,
                                      total_clauses=total_clauses,
                                      max_clause_size=max_clause_size)
        else:
            raise Exception('unknown value of k_clause')

        assert self.literal_gen.total_literals == self.required_literals, \
            f'Generator must produce {self.required_literals}, not {self.literal_gen.total_literals} literals'

    def __exact_constructor(self, literal_gen: LiteralGenerator, k_clauses: Dict[int, int]):
        self.k_clauses: Dict[int, int] = k_clauses
        self._total_clauses = sum(number_of_k for number_of_k in k_clauses.values())

        if literal_gen is None:
            # keep the default literal:clause ration 2:1
            self.literal_gen = KSATClauseGenerator._default_literal_generator(total_literals=self.required_literals)
        else:
            self.literal_gen = literal_gen

        KSATClauseGenerator._check_literal_generator_constraints(self.literal_gen, self._total_clauses,
                                                                 self.max_clause_size)

    def __random_constructor(self, literal_gen: LiteralGenerator, total_clauses: int, max_clause_size: int):

        if total_clauses < 1:
            raise Exception('number of clauses to generate can not be less than 1')

        if literal_gen is None:
            # keep the default literal:clause ration 2:1
            self.literal_gen = KSATClauseGenerator._default_literal_generator(total_literals=total_clauses * 2)
        else:
            self.literal_gen = literal_gen

        if max_clause_size is None:
            max_clause_size = ceil(self.literal_gen.total_literals / total_clauses) * 2
        elif max_clause_size < 1:
            raise Exception('max_clause_size can not be less than 1')

        KSATClauseGenerator._check_literal_generator_constraints(self.literal_gen, total_clauses, max_clause_size)

        self._total_clauses = total_clauses
        self.k_clauses = {}
        # take literal_gen.total_literals into consideration
        while total_clauses != 0:
            literals_left = self.literal_gen.total_literals - self.required_literals
            # help generator to end clause generation by putting all remaining variables to one clause
            if total_clauses == 1 and literals_left < max_clause_size:
                k = self.literal_gen.total_literals - self.required_literals
            else:
                k = random.randint(1, max_clause_size)

                # cover case, when there must be at least one literal per clause
                k = min(k, literals_left - total_clauses + 1)

                # cover case, when there are too many variables left for remaining clauses
                max_variables_consumed_by_remaining_clauses = (total_clauses - 1) * max_clause_size
                if literals_left - k > max_variables_consumed_by_remaining_clauses:
                    k = literals_left - max_variables_consumed_by_remaining_clauses

            total_clauses -= 1
            if self.k_clauses.get(k) is None:
                self.k_clauses[k] = 1
            else:
                self.k_clauses[k] += 1

    @staticmethod
    def _check_literal_generator_constraints(literal_gen, total_clauses, max_clause_size):
        if literal_gen.total_literals < total_clauses:
            raise Exception('There are not enough variables in given variable generator, '
                            f'should be more than {total_clauses}. There must be at least one literal per clause')
        if literal_gen.total_literals > max_clause_size * total_clauses:
            raise Exception('There are too many variables in variable generator, '
                            f'should be less than {max_clause_size * total_clauses}, is {literal_gen.total_literals}')

    @staticmethod
    def _default_literal_generator(total_literals: int):
        return RandomLiteralGenerator(total_literals=total_literals,
                                      unique_literals=0.75,
                                      negate_probability=0.5,
                                      predicate_generators=[ConstantGenerator(predicate_name='constant')])

    @property
    def total_clauses(self):
        return self._total_clauses

    @property
    def max_clause_size(self):
        return max(k for k in self.k_clauses.keys())

    @property
    def required_literals(self):
        return sum(k * number_of_k for k, number_of_k in self.k_clauses.items())

    @property
    def generated_clauses(self) -> int:
        return len(self._generated_clauses)

    @property
    def clause(self) -> Clause:
        if self.clauses_left == 0:
            raise StopIteration()

        keys = list(self.k_clauses.keys())
        while True:
            next_clause_size = random.choice(keys)
            # optimize: introduce state pattern instead copy
            lit_gen_state = copy.deepcopy(self.literal_gen)

            literals = set()

            while len(literals) != next_clause_size:
                lit_gen_state_loop = copy.deepcopy(self.literal_gen)
                lit = self.literal_gen.literal
                if lit in literals:
                    self.literal_gen = lit_gen_state_loop
                    continue
                literals.add(lit)
            assert all(literals), 'there is None element in literals'

            clause = Clause(total_literals=literals)
            if clause not in self._generated_clauses:
                self._generated_clauses.add(clause)
                self.k_clauses[next_clause_size] -= 1
                if self.k_clauses[next_clause_size] == 0:
                    del self.k_clauses[next_clause_size]
                return clause
            else:
                self.literal_gen = lit_gen_state


if __name__ == '__main__':

    from src.atom import ConstantGenerator, SafetyGenerator, LivenessGenerator, Atom, Atom, Atom

    lit_gen = RandomLiteralGenerator(total_literals=10,
                                     unique_literals=5,
                                     predicate_generators=[
                                         ConstantGenerator(predicate_name='constant'),
                                         SafetyGenerator(predicate_name='safety', argument='A'),
                                         LivenessGenerator(predicate_name='liveness', argument='a')
                                     ])
    clause_gen1 = KSATClauseGenerator(k_clauses={2: 5},
                                      literal_gen=lit_gen)
    cl = list(clause_gen1)
    for c in cl:
        if not c.literals:
            print("none!!!!")
    from pprint import pprint

    pprint([c.to_tptp() for c in cl])
