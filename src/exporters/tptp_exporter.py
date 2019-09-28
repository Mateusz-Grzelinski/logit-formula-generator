from __future__ import annotations

import textwrap
from dataclasses import field, dataclass
from typing import Union, Optional, Set, List

from src.ast.fol import Atom, CNFClause, Functor, Predicate, Variable, CNFFormula


def _print_arity(arities: Set[int]):
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


class TPTPExporter:
    @staticmethod
    def cnf_export(expression: Union[Functor, Variable, Predicate, Atom, Literal, CNFClause, CNFFormula]) -> str:
        raise NotImplemented


@dataclass
class TPTPHeader:
    seed: int = '-'
    version: str = '-'
    output_file: str = ''
    comment_sign: str = '%'
    line_separator: str = '-' * 76

    number_of_clause_instances: Optional[int] = None
    max_clause_size: Optional[int] = None
    number_of_unit_clauses: Optional[int] = None
    number_of_horn_clauses: Optional[int] = None
    number_of_RR_clauses: Optional[int] = None
    average_clause_size: Optional[int] = None

    number_of_literal_instances: Optional[int] = None
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

    def read_from(self, object: CNFFormula):
        if isinstance(object, CNFFormula):
            self.number_of_clause_instances = object.number_of_clause_instances
            self.max_clause_size = object.max_clause_size
            self.average_clause_size = object.average_clause_size
            self.number_of_unit_clauses = object.number_of_unit_clauses

            self.number_of_literal_instances = object.number_of_literal_instances
            # self.total_number_of_negated_literals = object.total_number_of_negated_literals

            self.number_of_atom_instances = object.number_of_atom_instances

            # self.predicate_arities = set(object.predicate_arities.keys())
            self.number_of_predicates = object.number_of_predicates

            self.number_of_variables = object.number_of_variable_instances
            self.number_of_singleton_variables = object.number_of_singleton_variables

            # self.functor_arities = set(object.functor_arities.keys())
            self.number_of_functors = object.number_of_functors
            self.number_of_constant_functors = object.number_of_constant_functors
            self.number_of_functors_instances = object.number_of_functor_instances

            self.max_term_depth = object.max_recursion_depth
        else:
            raise Exception('object type not supported')

    def get_header(self):
        file = f'{self.output_file} {self.version}'

        class RowEntry:
            def __init__(self, name: str, value: int, details: List):
                self.name = name
                self.value = value
                self.details = details

            def __str__(self):
                return f'{self.name} : {self.value} ({self.details})'

        syntax = dict(
            number_of_clauses=['Number of clauses', self.number_of_clause_instances, self.number_of_horn_clauses,
                               self.number_of_unit_clauses, self.number_of_RR_clauses],
            number_of_atoms=['Number of atoms', self.number_of_atom_instances, self.number_of_equality_atom_instances],
            maximal_clause_size=['Maximal clause size', self.max_clause_size, int(self.average_clause_size)],
            number_of_predicates=['Number of predicates', self.number_of_predicates,
                                  self.number_of_propositional_predicates, _print_arity(self.predicate_arities)],
            number_of_functors=['Number of functors', self.number_of_functors, self.number_of_constant_functors,
                                _print_arity(self.functor_arities)],
            number_of_variables=['Number of variables', self.number_of_variables, self.number_of_singleton_variables],
            maximal_term_depth=['Maximal term depth', self.max_term_depth, self.average_term_depth],
        )

        for key, value in syntax.items():
            for i, item in enumerate(value):
                if item is None:
                    value[i] = '-'
                else:
                    value[i] = str(item)

                if i == 0:
                    value[i] = value[i].ljust(22)
                elif i == 1:
                    value[i] = value[i].rjust(4)
                elif i == 2:
                    value[i] = value[i].rjust(3)

        syntax_text = [
            f'{syntax["number_of_clauses"][0]}: '
            f'{syntax["number_of_clauses"][1]} '
            f'( {syntax["number_of_clauses"][2]} non-Horn; '
            f'{syntax["number_of_clauses"][3]} unit; '
            f'{syntax["number_of_clauses"][4]} RR)\n',

            f'{syntax["number_of_atoms"][0]}: '
            f'{syntax["number_of_atoms"][1]} '
            f'( {syntax["number_of_atoms"][2]} equality)\n',

            f'{syntax["maximal_clause_size"][0]}: '
            f'{syntax["maximal_clause_size"][1]} '
            f'( {syntax["maximal_clause_size"][2]} average)\n',

            f'{syntax["number_of_predicates"][0]}: '
            f'{syntax["number_of_predicates"][1]} '
            f'( {syntax["number_of_predicates"][2]} propositional; '
            f'{syntax["number_of_predicates"][3]} arity)\n',

            f'{syntax["number_of_functors"][0]}: '
            f'{syntax["number_of_functors"][1]} '
            f'( {syntax["number_of_functors"][2]} constant; '
            f'{syntax["number_of_functors"][3]} arity)\n',

            f'{syntax["number_of_variables"][0]}: '
            f'{syntax["number_of_variables"][1]} '
            f'( {syntax["number_of_variables"][2]} singleton)\n',

            f'{syntax["maximal_term_depth"][0]}: '
            f'{syntax["maximal_term_depth"][1]} '
            f'( {syntax["maximal_term_depth"][2]} average)\n',
        ]

        text = f'{self.line_separator}\n' \
               f'File      : {file:<4}\n' \
               f'Syntax    : {(12 * " ").join(syntax_text)}\n' \
               f'{self.line_separator}\n'

        text = textwrap.indent(text=text, prefix=f'{self.comment_sign} ', predicate=lambda line: True)
        return text


if __name__ == '__main__':
    tptp_h = TPTPHeader()
    s = tptp_h.get_header()
    print(s)
