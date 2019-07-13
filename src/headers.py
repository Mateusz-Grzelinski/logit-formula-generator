from dataclasses import dataclass
from typing import Union


@dataclass
class TPTPHeader:
    seed: int = ''
    version: str = ''
    output_file: str = ''
    comment_sign: str = '%'
    total_literals: Union[int, str] = '-'
    unique_literals: Union[int, str] = '-'
    negate_probability: Union[int, str] = '-'
    total_clauses: Union[int, str] = '-'
    max_clause_size: Union[int, str] = '-'

    def get_header(self, format='tptp'):
        if format == 'tptp':
            return self._get_tptp_header()
        else:
            raise Exception(f'Unknown format value: {format}')

    def _get_tptp_header(self):
        max_r_just = max(len(str(attribute)) for attribute in dir(self) if not attribute.startswith('_'))

        def r_just(value):
            return str(value).rjust(max_r_just)

        cnf_header = f'''
    {'-' * 76}
    File     : {self.output_file} : logic-formula-generator {self.version}
    Syntax   : Number of clauses     :{r_just(self.total_clauses)} ({r_just('-')} non-Horn;{r_just('-')} unit;{r_just(
            '-')} RR)
    Number of atoms       :{r_just(self.total_literals)} ({r_just('-')} equality)
    Maximal clause size   :{r_just(self.max_clause_size)} ({r_just('-')} average)
    Number of predicates  :{r_just(self.unique_literals)} ({r_just('-')} propositional;{r_just(
            '0-0')} arity)
    Number of functors    :{r_just(0)} ({r_just(0)} constant;{r_just('---')} arity)
    Number of variables   :{r_just(0)} ({r_just(0)} singleton)
    Maximal term depth    :{r_just(1)} ({r_just(1)} average)
    {'-' * 76}

    Comments : generator sources available at https://github.com/Mateusz-Grzelinski/logit-formula-generator
    negate probability    :{r_just(self.negate_probability)}
    seed                  :{r_just(self.seed)}
    '''
        return cnf_header
