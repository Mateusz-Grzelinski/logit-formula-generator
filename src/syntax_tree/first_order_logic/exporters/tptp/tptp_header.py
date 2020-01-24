from __future__ import annotations

import textwrap
from dataclasses import field, dataclass
from typing import Optional, Set, Dict, Any

import src.syntax_tree.first_order_logic as fol


def _print_arity(arities: Set[int]) -> str:
    if not arities:
        return '-'

    ranges = []
    # iter = sorted(arities)
    # groupby(iter, lambda n, c=count(): n - next(c))
    previous_number = min(arities)
    for number in sorted(arities):
        if number != previous_number + 1:
            ranges.append([number])
        elif len(ranges[-1]) > 1:
            ranges[-1][-1] = number
        else:
            ranges[-1].append(number)
        previous_number = number
    return ','.join(['-'.join(map(str, range)) for range in ranges])


@dataclass
class _HeaderItem:
    name: str
    value: Any
    details: Dict[str, Any]

    def __str__(self):
        details = []
        for key, value in self.details.items():
            if value is None:
                value = '-'
            details.append(f'{str(value).rjust(3)} {str(key)}')
        details = '; '.join(details)

        value = '-' if self.value is None else str(self.value)
        return f'{self.name.ljust(22)}:{value.rjust(5)} ({details})\n'


@dataclass
class TPTPHeader:
    seed: int = '-'
    version: str = ''
    output_file: str = ''
    comment_sign: str = '%'
    line_separator: str = '-' * 76

    number_of_clause_instances: Optional[int] = None
    max_clause_size: Optional[int] = None
    number_of_unit_clauses: Optional[int] = None
    number_of_non_horn_clauses: Optional[int] = None
    number_of_RR_clauses: Optional[int] = None
    average_clause_size: Optional[int] = None

    # number_of_literal_instances: Optional[int] = None
    number_of_negated_literal_instances: Optional[int] = None

    number_of_atom_instances: Optional[int] = None
    number_of_equality_atom_instances: Optional[int] = None

    predicate_arities: Set[int] = field(default_factory=set)
    number_of_predicates: Optional[int] = None
    number_of_propositional_predicates: Optional[int] = None

    functor_arities: Set[int] = field(default_factory=set)
    number_of_functors: Optional[int] = None
    number_of_constant_functors: Optional[int] = None
    number_of_functors_instances: Optional[int] = None

    number_of_variables: Optional[int] = None
    number_of_singleton_variables: Optional[int] = None

    max_term_depth: Optional[int] = None
    average_term_depth: Optional[int] = None

    def read_from(self, object: fol.CNFFormulaInfo):
        if isinstance(object, fol.CNFFormulaInfo):
            self.number_of_clause_instances = object.number_of_instances[fol.CNFClause.__name__]
            self.max_clause_size = object.max_clause_size
            self.average_clause_size = int(object.average_clause_size)
            self.number_of_unit_clauses = object.number_of_unit_clauses
            self.number_of_non_horn_clauses = object.number_of_instances[
                                                  fol.CNFClause.__name__] - object.number_of_horn_clauses_instances

            # self.number_of_literal_instances = object.number_of_instances[Literal.__name__]
            self.number_of_negated_literal_instances = object.number_of_negated_literal_instances
            self.number_of_atom_instances = object.number_of_instances[fol.Atom.__name__]
            self.number_of_equality_atom_instances = object.number_of_equality_atom_instances

            self.predicate_arities = set(object.predicate_arities.keys())
            self.number_of_predicates = object.number_of[fol.Predicate.__name__]
            self.number_of_propositional_predicates = object.number_of_propositional_predicates

            self.number_of_variables = object.number_of_instances[fol.Variable.__name__]
            self.number_of_singleton_variables = object.number_of_singleton_variables

            self.functor_arities = set(object.functor_arities.keys())
            self.number_of_functors = object.number_of[fol.Functor.__name__]
            self.number_of_constant_functors = object.number_of_constant_functors
            self.number_of_functors_instances = object.number_of_instances[fol.Functor.__name__]

            self.max_term_depth = object.max_term_depth
        else:
            raise Exception('object type not supported')

    def get_header(self) -> str:
        file = f'{self.output_file} {self.version}'
        syntax_items = [
            _HeaderItem(
                name='Number of clauses', value=self.number_of_clause_instances,
                details={
                    'non-Horn': self.number_of_non_horn_clauses,
                    'unit': self.number_of_unit_clauses,
                    'RR': self.number_of_RR_clauses
                }),
            _HeaderItem(
                name='Number of atoms', value=self.number_of_atom_instances,
                details={
                    'equality': self.number_of_equality_atom_instances,
                }),
            _HeaderItem(
                name='Maximal clause size', value=self.max_clause_size,
                details={
                    'average': self.average_clause_size,
                }),
            _HeaderItem(
                name='Number of predicates', value=self.number_of_predicates,
                details={
                    'propositional': self.number_of_propositional_predicates,
                    'arity': _print_arity(self.predicate_arities),
                }),
            _HeaderItem(
                name='Number of functors', value=self.number_of_functors,
                details={
                    'constant': self.number_of_constant_functors,
                    'arity': _print_arity(self.functor_arities),
                }),
            _HeaderItem(
                name='Number of variables', value=self.number_of_variables,
                details={
                    'singleton': self.number_of_singleton_variables,
                }),
            _HeaderItem(
                name='Maximal term depth', value=self.max_term_depth,
                details={
                    'average': self.average_term_depth,
                }),
        ]

        text = f'{self.line_separator}\n' \
               f'File      : {file:<4}\n' \
               f'Syntax    : {(12 * " ").join(str(i) for i in syntax_items)}\n' \
               f'{self.line_separator}\n'

        text = textwrap.indent(text=text, prefix=f'{self.comment_sign} ', predicate=lambda line: True)
        return text
