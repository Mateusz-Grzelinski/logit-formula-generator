from dataclasses import dataclass
from typing import Union

from src.formula import Formula


@dataclass
class TPTPHeader:
    seed: int = '-'
    version: str = '-'
    output_file: str = ''
    comment_sign: str = '%'
    number_of_atoms: Union[int, str] = '-'
    max_clause_size: Union[int, str] = '-'
    number_of_predicates: Union[int, str] = '-'
    number_of_functors: Union[int, str] = '-'
    number_of_variables: Union[int, str] = '-'
    max_term_depth: Union[int, str] = '-'
    negated_literals: Union[int, str] = '-'
    number_of_clauses: Union[int, str] = '-'

    def read_from(self, object: Formula):
        if isinstance(object, Formula):
            self.number_of_clauses = object.number_of_clauses
            self.number_of_atoms = object.number_of_atoms
            self.max_clause_size = object.max_clause_size
            self.number_of_predicates = object.number_of_predicates
            self.number_of_functors = object.number_of_functors
            self.number_of_variables = object.number_of_variables
            self.max_term_depth = object.max_term_depth
            self.negated_literals = object.number_of_negated_literals
        else:
            raise Exception('object type not supported')

    def get_header(self, format='tptp'):
        if format == 'tptp':
            return self._get_tptp_header()
        else:
            raise Exception(f'Unknown format value: {format}')

    def _get_tptp_header(self):

        max_r_just = max(
            len(str(self.number_of_clauses)),
            len(str(self.number_of_atoms)),
            len(str(self.max_clause_size)),
            len(str(self.number_of_predicates)),
            len(str(self.number_of_functors)),
            len(str(self.number_of_variables)),
            len(str(self.max_term_depth)),
            len(str(self.negated_literals)) + 1)
        max_r_just = max(max_r_just, 4)

        def r_just(value=None):
            if value is None:
                return '-'.rjust(max_r_just)
            else:
                return str(value).rjust(max_r_just)

        cnf_header = f'''
{'-' * 76}
File     : {self.output_file} : logic-formula-generator {self.version}
Syntax   : Number of clauses     :{r_just(self.number_of_clauses)} ({r_just()} non-Horn;{r_just()} unit;{r_just()} RR)
           Number of atoms       :{r_just(self.number_of_atoms)} ({r_just()} equality)
           Maximal clause size   :{r_just(self.max_clause_size)} ({r_just()} average)
           Number of predicates  :{r_just(self.number_of_predicates)} ({r_just()} propositional;{r_just()} arity)
           Number of functors    :{r_just(self.number_of_functors)} ({r_just()} constant;{r_just()} arity)
           Number of variables   :{r_just(self.number_of_variables)} ({r_just()} singleton)
           Maximal term depth    :{r_just(self.max_term_depth)} ({r_just()} average)
{'-' * 76}

Comments : generator sources available at https://github.com/Mateusz-Grzelinski/logit-formula-generator
negated_literals      :{r_just(self.negated_literals)}
seed                  :{r_just(self.seed)}
'''
        return f'\n{self.comment_sign} '.join(line for line in cnf_header.splitlines()) + '\n'
