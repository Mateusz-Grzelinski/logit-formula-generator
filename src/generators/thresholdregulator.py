from typing import Iterable, List

from src.ast.fol import CNFFormula, CNFClause
from src.generators.randomcnfgenerator import RandomCNFGenerator
from src.placeholders.fol import CNFClausePlaceholder


class ThresholdRegulator:
    def __init__(self,
                 number_of_variables: Iterable[int],
                 number_of_functors: Iterable[int],
                 number_of_predicates: Iterable[int],
                 number_of_atoms: Iterable[int],
                 number_of_literals: Iterable[int],
                 number_of_clauses: Iterable[int]):
        self.allowed_number_of_clauses = set(number_of_clauses) if number_of_clauses is not None else None
        self.allowed_number_of_literals = set(number_of_literals) if number_of_literals is not None else None
        self.allowed_number_of_atoms = set(number_of_atoms) if number_of_atoms is not None else None
        self.allowed_number_of_predicates = set(number_of_predicates) if number_of_predicates is not None else None
        self.allowed_number_of_functors = set(number_of_functors) if number_of_functors is not None else None
        self.allowed_number_of_variables = set(number_of_variables) if number_of_variables is not None else None

    @staticmethod
    def range(number: int, threshold: float = None, delta: int = None) -> List[int]:
        if threshold is None and delta is None:
            raise AttributeError('one of threshold or delta must be defined')
        elif threshold is None:
            return [i for i in range(int(number - delta), int(number + delta)) if i >= 0]
        elif delta is None:
            delta_from_threshold = number * threshold
            return [i for i in range(int(number - delta_from_threshold), int(number + delta_from_threshold)) if i >= 0]
        else:
            delta_from_threshold = number * threshold
            return [i for i in range(min(int(number - delta_from_threshold), number + delta),
                                     max(int(number + delta_from_threshold), number + delta)) if i >= 0]

    def tune_cnf_formula(self, generator: RandomCNFGenerator, initial_cnf_formula: CNFFormula):
        self._fix_number_of_literals(generator, initial_cnf_formula)

        if self.allowed_number_of_atoms and initial_cnf_formula.number_of_atoms not in self.allowed_number_of_atoms:
            pass
        if self.allowed_number_of_predicates and initial_cnf_formula.number_of_predicates not in self.allowed_number_of_predicates:
            pass
        if self.allowed_number_of_functors and initial_cnf_formula.number_of_functors not in self.allowed_number_of_functors:
            pass
        if self.allowed_number_of_variables and initial_cnf_formula.number_of_variables not in self.allowed_number_of_variables:
            pass
        # todo check for duplicated clauses

    def _fix_number_of_literals(self, generator: RandomCNFGenerator, formula: CNFFormula):
        min_allowed_number_of_literals = min(self.allowed_number_of_literals)
        max_allowed_number_of_literals = max(self.allowed_number_of_literals)

        sorted_placeholder_clauses = sorted(generator.ast_elements[CNFClause].keys(), key=len)
        max_placeholder_length = len(sorted_placeholder_clauses[-1])
        exit_loop = False
        while not exit_loop:
            for cont, i, clause in formula.clauses(enum=True):
                needs_less_literals = max_allowed_number_of_literals < formula.number_of_literal_instances
                needs_more_literals = formula.number_of_literal_instances < min_allowed_number_of_literals
                if needs_less_literals:
                    literal_difference = formula.number_of_literal_instances - min_allowed_number_of_literals
                    literals_high_range = clause.number_of_literal_instances
                    literals_low_range = literals_high_range - literal_difference
                elif needs_more_literals:
                    literal_difference = max_allowed_number_of_literals - formula.number_of_literal_instances
                    literals_low_range = clause.number_of_literal_instances
                    literals_high_range = literals_low_range + literal_difference
                else:
                    exit_loop = True
                    break

                first_matching_placeholder = next(
                    (clause_placeholder for clause_placeholder in sorted_placeholder_clauses if
                     literals_low_range < clause_placeholder.number_of_literal_instances < literals_high_range),
                    None)

                if first_matching_placeholder is not None:
                    cont[i] = first_matching_placeholder
                elif all(clause.number_of_literal_instances == max_placeholder_length for clause in formula.clauses()):
                    raise Exception(f'You requested too many literals. '
                                    f'You want minimum {min_allowed_number_of_literals}, '
                                    f'but I can provide max {formula.number_of_literal_instances}')

        for cont, i, clause in formula.clauses(enum=True):
            if isinstance(clause, CNFClausePlaceholder):
                cont[i] = generator.recursive_generate(clause.instantiate())

    def _fix_number_of_clauses(self, generator: RandomCNFGenerator, initial_cnf_formula: CNFFormula):
        pass

    """
    Fixing strategies: (number of items outside threshold)
    a) literals
    - change clause weights
    b) atoms
    - change clause weights
    c) predicates
    - change clause weights
    - change atom weights (ex. less equality atoms)
    - reduce variability of predicates (p1, p2, p3 -> p)
    - exchange p -> v or vice versa
    ...
    
    c) use case: too little predicates
    
    1) remember state of generator
    2a) check if it is possible to reach required number of predicates with current clauses
    2b) if not exchange short clause for longer (within threshold)
    2b) change atoms weights to favor ones containing more predicates
    3) generate formula again? reset all atoms?
    4) if predicates still too low, go back to 1) Repeat until ?
    5) now we know that changing atoms is not enough. 
    6) change clause weights to favor longer ones
    """
