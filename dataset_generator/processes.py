import os

from src.formula import Formula
from src.headers import TPTPHeader

directory = '../test_data'


def save_test_file(formula: Formula, filename: str, dir: str = ''):
    global directory
    if not os.path.splitext(filename)[1]:
        filename += '.p'
    header = TPTPHeader()
    header.read_from(formula)
    header.version = 'not versioned'
    header.output_file = filename
    header.comment_sign = '%'

    if not os.path.isdir(directory):
        os.mkdir(directory)
    dir = os.path.join(directory, dir)
    if not os.path.isdir(dir):
        os.mkdir(dir)
    filename = os.path.join(dir, filename)

    with open(filename, 'w+') as file:
        file.truncate()
        file.write(header.get_header())
        for part in formula.to_tptp():
            file.write(part + '\n')


def generate_process(tuple):
    clause_gen, filename, dirname = tuple[0], tuple[1], tuple[2]
    formula = Formula(clauses=list(clause_gen))
    save_test_file(formula=formula, filename=filename, dir=dirname)
