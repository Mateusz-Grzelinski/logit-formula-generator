import os
import random
import time

from src.clause import KSATClauseGenerator
from src.formula import Formula
from src.headers import TPTPHeader
from src.literal import RandomLiteralGenerator
from src.predicate import SafetyGenerator, LivenessGenerator

seed = int(time.time() * 1000)
directory = 'test_data'


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


def dataset_1():
    for total_clauses in [100, 200, 500, 1000, 2500, 5000]:
        for ratio in [2, 3, 4, 5, 10]:
            print(f'generating dataset 1, total clauses {total_clauses}, ratio {ratio}')
            total_literals = total_clauses * ratio

            lit_gen = RandomLiteralGenerator(total_literals=total_literals,
                                             unique_literals=0.75,
                                             predicate_generator=[
                                                 # ConstantGenerator(predicate_name='constant'),
                                                 SafetyGenerator(predicate_name='safety', argument='A'),
                                                 LivenessGenerator(predicate_name='liveness', argument='a')
                                             ])
            clause_gen = KSATClauseGenerator(k_clauses='random',
                                             total_clauses=total_clauses,
                                             max_clause_size=total_literals // total_clauses,
                                             literal_gen=lit_gen)
            formula = Formula(clauses=list(clause_gen))
            save_test_file(formula=formula, filename=f'dataset1_{total_clauses}_{ratio}', dir='data_set_1')


if __name__ == '__main__':
    print('Starting')

    random.seed(seed)
    dataset_1()

    print('Finished')
