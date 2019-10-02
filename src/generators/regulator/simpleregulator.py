from typing import Iterable, NoReturn, Sized, Tuple, Union

from src.ast.fol import CNFFormula, CNFClause, Literal
from src.generators.randomcnfgenerator import RandomCNFGenerator
from src.generators.regulator.range import Range


def pick_next_shorter(population: Iterable[Sized], item: Sized):
    for i in population:
        difference = len(i) - len(item)
        if difference < 0:
            return i, difference
    return None, 0


def pick_next_longer(population: Iterable[Sized], item: Sized):
    for i in population:
        difference = len(i) - len(item)
        if difference > 0:
            return i, difference
    return None, 0


class SimpleRegulator:
    """Take only actions that will make formula better"""

    def __init__(self,
                 allowed_literal_range: Union[Range, Tuple[int, int]],
                 allowed_clause_range: Union[Range, Tuple[int, int]]):
        self.allowed_range = {
            CNFClause: Range(min=allowed_clause_range[0], max=allowed_clause_range[1]),
            Literal: Range(min=allowed_literal_range[0], max=allowed_literal_range[1]),
        }

    def tune_cnf_formula(self, generator: RandomCNFGenerator, initial_cnf_formula: CNFFormula):
        self._tune_number_of_clauses(generator, initial_cnf_formula)
        self._tune_number_of_literals(generator, initial_cnf_formula)
        generator.replace_inner_placeholders(initial_cnf_formula)

    def _tune_number_of_literals(self, generator: RandomCNFGenerator, formula: CNFFormula) -> NoReturn:
        min_allowed_number_of_literals = min(self.allowed_range[Literal])
        max_allowed_number_of_literals = max(self.allowed_range[Literal])

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
                    cont[i] = first_matching_placeholder.instantiate()
                elif all(clause.number_of_literal_instances == max_placeholder_length for clause in formula.clauses()):
                    raise Exception(f'You requested too many literals. '
                                    f'You want minimum {min_allowed_number_of_literals}, '
                                    f'but I can provide max {formula.number_of_literal_instances}')

    def _tune_number_of_clauses(self, generator: RandomCNFGenerator, initial_cnf_formula: CNFFormula):
        pass
