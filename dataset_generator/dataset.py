import random
import time
from multiprocessing.pool import Pool

from dataset_generator.processes import generate_process, save_test_file
from src.atom import SafetyGenerator, LivenessGenerator
from src.clause import KSATClauseGenerator
from src.formula import Formula, Mix, FormulaGenerator
from src.literal import RandomLiteralGenerator

seed = int(time.time() * 1000)
pool = Pool()
argument_queue = list()


def dataset_1():
    for total_clauses in [100, 200, 500, 1000, 2500, 5000]:
        for ratio in [2, 3, 4, 5, 10]:
            print(f'generating dataset 1, total clauses {total_clauses}, ratio {ratio}')
            total_literals = total_clauses * ratio

            lit_gen = RandomLiteralGenerator(total_literals=total_literals,
                                             unique_literals=0.75,
                                             predicate_generators=[
                                                 # ConstantGenerator(predicate_name='constant'),
                                                 SafetyGenerator(predicate_name='safety', argument='A'),
                                                 LivenessGenerator(predicate_name='liveness', argument='a')
                                             ])
            clause_gen = KSATClauseGenerator(k_clauses='random',
                                             total_clauses=total_clauses,
                                             max_clause_size=round(1.6 * total_literals // total_clauses),
                                             literal_gen=lit_gen)
            argument_queue.append((clause_gen, f'data_set1_{total_clauses}_{ratio}', 'data_set_1'))


def dataset_2():
    for total_clauses in [100, 200, 500, 1000, 2500, 5000]:
        for ratio in [2, 3, 4, 5, 10]:
            print(f'generating dataset 2, total clauses {total_clauses}, ratio {ratio}')
            total_literals = total_clauses * ratio

            lit_gen = RandomLiteralGenerator(total_literals=total_literals,
                                             unique_literals=0.75,
                                             predicate_generators_weights=[ratio, 1],
                                             predicate_generators=[
                                                 SafetyGenerator(predicate_name='safety', argument='A'),
                                                 LivenessGenerator(predicate_name='liveness', argument='a')
                                             ])
            clause_gen = KSATClauseGenerator(k_clauses='random',
                                             total_clauses=total_clauses,
                                             max_clause_size=round(1.6 * total_literals // total_clauses),
                                             literal_gen=lit_gen)
            argument_queue.append((clause_gen, f'data_set2_{total_clauses}_{ratio}:1', 'data_set_2'))

            lit_gen = RandomLiteralGenerator(total_literals=total_literals,
                                             unique_literals=0.75,
                                             predicate_generators_weights=[1, ratio],
                                             predicate_generators=[
                                                 SafetyGenerator(predicate_name='safety', argument='A'),
                                                 LivenessGenerator(predicate_name='liveness', argument='a')
                                             ])
            clause_gen = KSATClauseGenerator(k_clauses='random',
                                             total_clauses=total_clauses,
                                             max_clause_size=round(1.6 * total_literals // total_clauses),
                                             literal_gen=lit_gen)
            argument_queue.append((clause_gen, f'data_set2_{total_clauses}_1:{ratio}', 'data_set_2'))


def dataset_3():
    def generate(k_clauses):
        total_literals = sum(k * number_of_k for k, number_of_k in k_clauses.items())

        lit_gen = RandomLiteralGenerator(total_literals=total_literals,
                                         unique_literals=0.75,
                                         predicate_generators=[
                                             # ConstantGenerator(predicate_name='constant'),
                                             SafetyGenerator(predicate_name='safety', argument='A'),
                                             LivenessGenerator(predicate_name='liveness', argument='a')
                                         ])
        clause_gen = KSATClauseGenerator(k_clauses=k_clauses.copy(),
                                         literal_gen=lit_gen)
        formula = Formula(clauses=list(clause_gen))

        part_filename = [f'{key}:{value}' for key, value in k_clauses.items()]
        save_test_file(formula=formula, filename=f'dataset2_{total_clauses}_{"_".join(part_filename)}',
                       dir='data_set_2')

    for total_clauses in [100, 200, 300, 400, 500, 1000, 2500, 5000]:
        print(f'generating dataset 2, total clauses {total_clauses}')

        # part 1 - 4 equal
        k_clauses = {1: round(0.25 * total_clauses),
                     5: round(0.25 * total_clauses),
                     10: round(0.25 * total_clauses),
                     20: round(0.25 * total_clauses)}
        generate(k_clauses)

        # part 2 - 4, 1-SAT less
        k_clauses = {1: round(0.01 * total_clauses),
                     5: round(0.33 * total_clauses),
                     10: round(0.33 * total_clauses),
                     20: round(0.33 * total_clauses)}
        generate(k_clauses)

        # part 3 - 3 equal
        k_clauses = {1: round(1 / 3 * total_clauses),
                     5: round(1 / 3 * total_clauses),
                     10: round(1 / 3 * total_clauses)}
        generate(k_clauses)

        # part 4 - 4, 20-SAT less
        k_clauses = {1: round(0.33 * total_clauses),
                     5: round(0.33 * total_clauses),
                     10: round(0.33 * total_clauses),
                     20: round(0.01 * total_clauses)}
        generate(k_clauses)

        # part 5 - 4 equal
        k_clauses = {5: round(1 / 3 * total_clauses),
                     10: round(1 / 3 * total_clauses),
                     20: round(1 / 3 * total_clauses)}
        generate(k_clauses)


def dataset_4():
    def generate_clause_group():
        total_literals = 50
        total_clauses = random.randint(a=1, b=40)
        lit_gen = RandomLiteralGenerator(total_literals=total_literals,
                                         unique_literals=0.75,
                                         predicate_generators=[
                                             # ConstantGenerator(predicate_name='constant'),
                                             # todo make unique names
                                             SafetyGenerator(predicate_name='safety', argument='A'),
                                             LivenessGenerator(predicate_name='liveness', argument='a')
                                         ])
        clause_gen = KSATClauseGenerator(k_clauses='random',
                                         total_clauses=total_clauses,
                                         max_clause_size=round(1.6 * total_literals // total_clauses),
                                         literal_gen=lit_gen)
        return clause_gen

    for total_clauses in [100, 200, 500, 1000, 2500, 5000]:
        for number_of_clause_groups in [5, 10, 15, 20]:
            print(f'generating dataset 3, total clauses {total_clauses}, groups {number_of_clause_groups}')
            # todo generate groups only once
            # dataset3_1 - baseline - no mix ---------------------------------------------------------------------------
            clause_gens = [generate_clause_group() for _ in range(number_of_clause_groups)]

            formula_gen = FormulaGenerator(mixes=[], clause_generators=clause_gens)
            formula = formula_gen.generate()

            prefix = 'data_set_3_1'
            save_test_file(formula=formula, filename=f'{prefix}_{total_clauses}_{number_of_clause_groups}',
                           dir=f'{prefix}')

            # dataset3_2 - chain mix 2 groups per mix ------------------------------------------------------------------
            clause_gens = [generate_clause_group() for _ in range(number_of_clause_groups)]

            mixes = Mix.chain_mix(clause_groups_length=len(clause_gens), groups_per_mix=2)
            for mix in mixes:
                mix.number_of_literals = 50
                mix.number_of_clauses = 10

            formula_gen = FormulaGenerator(mixes=mixes, clause_generators=clause_gens)
            formula = formula_gen.generate()

            prefix = 'data_set_3_2'
            save_test_file(formula=formula, filename=f'{prefix}_{total_clauses}_{number_of_clause_groups}',
                           dir=f'{prefix}')

            # dataset3_3 - chain mix 3 groups per mix ------------------------------------------------------------------
            clause_gens = [generate_clause_group() for _ in range(number_of_clause_groups)]

            mixes = Mix.chain_mix(clause_groups_length=len(clause_gens), groups_per_mix=3)
            for mix in mixes:
                mix.number_of_literals = 50
                mix.number_of_clauses = 10

            formula_gen = FormulaGenerator(mixes=mixes, clause_generators=clause_gens)
            formula = formula_gen.generate()

            prefix = 'data_set_3_3'
            save_test_file(formula=formula, filename=f'{prefix}_{total_clauses}_{number_of_clause_groups}',
                           dir=f'{prefix}')

            # dataset3_4 - chain mix 4 groups per mix ------------------------------------------------------------------
            clause_gens = [generate_clause_group() for _ in range(number_of_clause_groups)]

            mixes = Mix.chain_mix(clause_groups_length=len(clause_gens), groups_per_mix=4)
            for mix in mixes:
                mix.number_of_literals = 50
                mix.number_of_clauses = 10

            formula_gen = FormulaGenerator(mixes=mixes, clause_generators=clause_gens)
            formula = formula_gen.generate()

            prefix = 'data_set_3_4'
            save_test_file(formula=formula, filename=f'{prefix}_{total_clauses}_{number_of_clause_groups}',
                           dir=f'{prefix}')

            # dataset3_5 - chain mix with skip -------------------------------------------------------------------------
            clause_gens = [generate_clause_group() for _ in range(number_of_clause_groups)]

            mixes = Mix.chain_mix(clause_groups_length=len(clause_gens), skip=1, groups_per_mix=2)
            for mix in mixes:
                mix.number_of_literals = 50
                mix.number_of_clauses = 10

            formula_gen = FormulaGenerator(mixes=mixes, clause_generators=clause_gens)
            formula = formula_gen.generate()

            prefix = 'data_set_3_5'
            save_test_file(formula=formula, filename=f'{prefix}_{total_clauses}_{number_of_clause_groups}',
                           dir=f'{prefix}')


if __name__ == '__main__':
    print('Starting')

    random.seed(seed)
    dataset_1()
    dataset_2()
    # dataset_3()
    # dataset_4()

    pool.map(generate_process, argument_queue)
    pool.close()
    print('All processes finished')
