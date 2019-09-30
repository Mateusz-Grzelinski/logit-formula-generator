from typing import Iterable, NoReturn, Type, Sized, Tuple, Union

from src.ast import AstElement
from src.ast.fol import CNFFormula, CNFClause, Atom, Literal, Functor, Variable, Predicate
from src.containers.fol import PredicateContainer
from src.generators.randomcnfgenerator import RandomCNFGenerator
from .correction import Correction, CorrectiveAction
from .exceptions import PropagateToParent
from .range import Range


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


class ThresholdRegulator:
    """Take only actions that will make formula better"""

    def __init__(self,
                 allowed_variable_range: Union[Range, Tuple[int, int]],
                 allowed_functor_range: Union[Range, Tuple[int, int]],
                 allowed_predicate_range: Union[Range, Tuple[int, int]],
                 # allowed_atom_range: Union[Range, Tuple[int, int]],
                 allowed_literal_range: Union[Range, Tuple[int, int]],
                 allowed_clause_range: Union[Range, Tuple[int, int]]):
        self.allowed_range = {
            CNFClause: Range(min=allowed_clause_range[0], max=allowed_clause_range[1]),
            Literal: Range(min=allowed_literal_range[0], max=allowed_literal_range[1]),
            Atom: Range(),
            Predicate: Range(min=allowed_predicate_range[0], max=allowed_predicate_range[1]),
            Functor: Range(min=allowed_functor_range[0], max=allowed_functor_range[1]),
            Variable: Range(min=allowed_variable_range[0], max=allowed_variable_range[1]),
        }
        self.correction_ranges = {
            CNFClause: None,
            Literal: None,
            Atom: None,
            Predicate: None,
            Functor: None,
            Variable: None,
        }

    @staticmethod
    def range(number: int, threshold: float = None, delta: int = None) -> Tuple[int, int]:
        if threshold is None and delta is None:
            raise AttributeError('one of threshold or delta must be defined')
        elif threshold is None:
            return int(number - delta), int(number + delta)
        elif delta is None:
            delta_from_threshold = number * threshold
            return int(number - delta_from_threshold), int(number + delta_from_threshold)
        else:
            delta_from_threshold = number * threshold
            return min(int(number - delta_from_threshold), number + delta), max(int(number + delta_from_threshold),
                                                                                number + delta)

    def tune_cnf_formula(self, generator: RandomCNFGenerator, initial_cnf_formula: CNFFormula):
        self._tune_number_of_literals(generator, initial_cnf_formula)
        # self._tune_number_of_clauses(generator, initial_cnf_formula)

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

        generator.replace_inner_placeholders(formula)

    def _calculate_correction(self, ast_type: Type[AstElement], formula: CNFFormula) -> Correction:
        # todo
        number_of_ast_element = formula.number_of_instances(ast_type)
        needs_less = self.allowed_range[ast_type].max < number_of_ast_element
        needs_more = number_of_ast_element < self.allowed_range[ast_type].min
        correction_info = Correction()
        if needs_less:
            correction_info.action = CorrectiveAction.SHRINK
            correction_info.correction_range.min = max(0, self.allowed_range[ast_type].min - number_of_ast_element)
            correction_info.correction_range.max = max(0, self.allowed_range[ast_type].max - number_of_ast_element)
        elif needs_more:
            correction_info.action = CorrectiveAction.GROW
            correction_info.correction_range.min = max(0, self.allowed_range[ast_type].min - number_of_ast_element)
            correction_info.correction_range.max = max(0, self.allowed_range[ast_type].max - number_of_ast_element)
        return correction_info

    def _tune_number_of_clauses(self, generator: RandomCNFGenerator, formula: CNFFormula) -> NoReturn:
        clause_correction = self._calculate_correction(ast_type=CNFClause, formula=formula)
        literal_correction = self._calculate_correction(ast_type=CNFClause.direct_children_types, formula=formula)
        available_placeholders = sorted(generator.ast_elements[Literal].keys(), key=len)
        if literal_correction.action == CorrectiveAction.SHRINK:
            correction_method = pick_next_shorter
        elif literal_correction.action == CorrectiveAction.GROW:
            correction_method = pick_next_longer
        else:
            assert False

        corrected_by = 0
        while True:
            formula_was_changed = False
            for container, i, item in formula.items(type=PredicateContainer, enum=True):  # todo random=True?
                if not isinstance(item, Literal):
                    continue
                first_matching_placeholder, difference = correction_method(population=available_placeholders,
                                                                           item=container)
                if first_matching_placeholder is not None:
                    container[i] = first_matching_placeholder.instantiate()
                    formula_was_changed = True
                    corrected_by += difference
                    if corrected_by in literal_correction.correction_range:
                        return
                    elif corrected_by > literal_correction.correction_range.max:
                        # you over done it, pick opposite method
                        correction_method = pick_next_shorter if correction_method == pick_next_longer else pick_next_longer
                    elif corrected_by < literal_correction.correction_range.min:
                        # keep going
                        pass

            """
            - replace item with placeholder
            - replace atom with atom with more items
            - add more literal 
            - 
            """
            if not formula_was_changed:
                raise PropagateToParent(
                    f'You requested too little atoms. You want minimum {min(self.allowed_range[Atom])}, '
                    f'but I can provide minimum {formula.number_of_instances[Atom]}',
                    failing_ast_element=Atom,
                    required_correction=Correction(action=literal_correction.action,
                                                   correction_range=Range(
                                                       min=literal_correction.correction_range.min - corrected_by,
                                                       max=literal_correction.correction_range.max - corrected_by)
                                                   )
                )

    def _tune_number_of_predicates(self, generator: RandomCNFGenerator, formula: CNFFormula,
                                   ) -> NoReturn:
        # todo sort by len and by weight?
        # todo it should be {1: [p, v], 2: [p =p, v = v, p =v, ...]}
        clause_correction = self._calculate_correction(ast_type=CNFClause, formula=formula)
        literal_correction = self._calculate_correction(ast_type=Literal, formula=formula)
        predicate_correction = self._calculate_correction(ast_type=Predicate, formula=formula)
        available_placeholders = sorted(generator.ast_elements[Predicate].keys(), key=len)
        if predicate_correction.action == CorrectiveAction.SHRINK:
            correction_method = pick_next_shorter
        elif predicate_correction.action == CorrectiveAction.GROW:
            correction_method = pick_next_longer
        else:
            assert False

        corrected_by = 0
        while True:
            formula_was_changed = False
            for container, i, item in formula.items(type=PredicateContainer, enum=True):  # todo random=True?
                if not isinstance(item, Predicate):
                    continue
                first_matching_placeholder, difference = correction_method(population=available_placeholders,
                                                                           item=container)
                if first_matching_placeholder is not None:
                    container[i] = first_matching_placeholder.instantiate()
                    formula_was_changed = True
                    corrected_by += difference
                    if corrected_by in predicate_correction.correction_range:
                        return
                    elif corrected_by > predicate_correction.correction_range.max:
                        # you over done it, pick opposite method
                        correction_method = pick_next_shorter if correction_method == pick_next_longer else pick_next_longer
                    elif corrected_by < predicate_correction.correction_range.min:
                        # keep going
                        pass

            """
            - replace item with placeholder
            - replace atom with atom with more items
            - add more literal 
            - 
            """
            if not formula_was_changed:
                raise PropagateToParent(
                    f'You requested too little atoms. You want minimum {min(self.allowed_range[Atom])}, '
                    f'but I can provide minimum {formula.number_of_instances[Atom]}',
                    failing_ast_element=Atom,
                    required_correction=Correction(action=predicate_correction.action,
                                                   correction_range=Range(
                                                       min=predicate_correction.correction_range.min - corrected_by,
                                                       max=predicate_correction.correction_range.max - corrected_by)
                                                   )
                )
