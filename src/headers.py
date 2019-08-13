from dataclasses import dataclass, field
from typing import Set, Optional

from src.formula import Formula


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


@dataclass
class TPTPHeader:
    seed: int = '-'
    version: str = '-'
    output_file: str = ''
    comment_sign: str = '%'
    number_of_atoms: Optional[int] = None
    number_of_literals: Optional[int] = None
    total_number_of_literals: Optional[int] = None
    max_clause_size: Optional[int] = None
    number_of_predicates: Optional[int] = None
    predicate_arities: Set[int] = field(default_factory=set)
    number_of_functors: Optional[int] = None
    total_number_of_functors: Optional[int] = None
    functor_arities: Set[int] = field(default_factory=set)
    number_of_variables: Optional[int] = None
    total_number_of_variables: Optional[int] = None
    max_term_depth: Optional[int] = None
    total_number_of_negated_literals: Optional[int] = None
    number_of_clauses: Optional[int] = None
    average_clause_size: Optional[int] = None
    number_of_unit_clauses: Optional[int] = None
    number_of_singleton_variables: Optional[int] = None

    def read_from(self, object: Formula):
        if isinstance(object, Formula):
            self.number_of_clauses = object.number_of_clauses
            self.number_of_literals = object.number_of_literals
            self.total_number_of_literals = object.total_number_of_literals
            self.number_of_atoms = object.number_of_atoms
            self.max_clause_size = object.max_clause_size
            self.number_of_predicates = object.number_of_predicates
            self.predicate_arities = set(object.predicate_arities.keys())
            self.functor_arities = set(object.functor_arities.keys())
            # total_number_of_predicates is (in current version) the same as number of atoms
            self.total_number_of_variables = object.total_number_of_variables
            self.total_number_of_functors = object.total_number_of_functors
            self.number_of_functors = object.number_of_functors
            self.number_of_variables = object.number_of_variables
            self.max_term_depth = object.max_term_depth
            self.total_number_of_negated_literals = object.total_number_of_negated_literals
            self.average_clause_size = object.average_clause_size
            self.number_of_unit_clauses = object.number_of_unit_clauses
            self.number_of_singleton_variables = object.number_of_singleton_variables
        else:
            raise Exception('object type not supported')

    def get_header(self, format='tptp'):
        if format == 'tptp':
            return self._get_tptp_header()
        else:
            raise Exception(f'Unknown format value: {format}')

    def _get_tptp_header(self):

        # keep the first column nicely aligned
        # align to longest number + 1, minimum 4
        max_r_just = max(
            len(str(self.number_of_clauses)),
            len(str(self.number_of_atoms)),
            len(str(self.max_clause_size)),
            len(str(self.number_of_predicates)),
            len(str(self.number_of_functors)),
            len(str(self.number_of_variables)),
            len(str(self.max_term_depth)),
            len(str(self.total_number_of_negated_literals)),
            len(str(self.average_clause_size)),
            len(str(self.number_of_unit_clauses)),
            len(str(self.number_of_singleton_variables)) + 1)
        max_r_just = max(max_r_just, 4)

        def r_just(value=None):
            if value is None:
                return '-'.rjust(max_r_just)
            else:
                return str(value).rjust(max_r_just)

        cnf_header = f'''
{'-' * 76}
File     : {self.output_file} : logic-formula-generator {self.version}
Syntax   : Number of clauses     :{r_just(self.number_of_clauses)} ({r_just()} non-Horn;{r_just(self.number_of_unit_clauses)} unit;{r_just()} RR)
           Number of atoms       :{r_just(self.number_of_atoms)} ({r_just()} equality)
           Maximal clause size   :{r_just(self.max_clause_size)} ({r_just(self.average_clause_size)} average)
           Number of predicates  :{r_just(self.number_of_predicates)} ({r_just()} propositional; {_print_arity(self.predicate_arities)} arity) 
           Number of functors    :{r_just(self.number_of_functors)} ({r_just(self.number_of_functors)} constant; {_print_arity(self.functor_arities)} arity)
           Number of variables   :{r_just(self.number_of_variables)} ({r_just(self.number_of_singleton_variables)} singleton)
           Maximal term depth    :{r_just(self.max_term_depth)} ({r_just()} average)
{'-' * 76}

Comments : generator sources available at https://github.com/Mateusz-Grzelinski/logit-formula-generator
Total number of literals :{r_just(self.total_number_of_literals)}
Number of literals       :{r_just(self.number_of_literals)}
Total negated literals   :{r_just(self.total_number_of_negated_literals)}
Seed                     :{r_just(self.seed)}
Total functors           :{r_just(self.total_number_of_functors)}
Total variables          :{r_just(self.total_number_of_variables)}

'''
        return f'\n{self.comment_sign} '.join(line for line in cnf_header.splitlines()) + '\n'
