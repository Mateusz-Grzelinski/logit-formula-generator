import argparse
import random
import sys
import time
from math import ceil
from typing import Tuple

from src.clause import KSATClauseGenerator
from src.literal import RandomLiteralGenerator

version = 'Pre-alpha 0.1'
bug_message = 'this shouldn\'t happen. This is bug'


def print_header(lit_gen: RandomLiteralGenerator,
                 clause_gen: KSATClauseGenerator,
                 seed: int,
                 output_file: str = None,
                 comment_sign: str = '%'):
    r_justed = lambda value: str(value).rjust(5)
    output_file = 'stdout' if output_file is None else output_file
    cnf_header = f'''
{'-' * 76}
File     : {output_file} : logic-formula-generator {version}
Syntax   : Number of clauses     :{r_justed(clause_gen.total_clauses)} ({r_justed('-')} non-Horn;{r_justed(
        '-')} unit;{r_justed('-')} RR)
           Number of atoms       :{r_justed(lit_gen.total_literals)} ({r_justed('-')} equality)
           Maximal clause total_number_of_literals   :{r_justed(clause_gen.max_clause_size)} ({r_justed('-')} average)
           Number of predicates  :{r_justed(lit_gen.unique_literals)} ({r_justed('-')} propositional;{r_justed(
        '0-0')} arity)
           Number of functors    :{r_justed(0)} ({r_justed(0)} constant;{r_justed('---')} arity)
           Number of variables   :{r_justed(0)} ({r_justed(0)} singleton)
           Maximal term depth    :{r_justed(1)} ({r_justed(1)} average)
{'-' * 76}

Comments : generator sources available at https://github.com/Mateusz-Grzelinski/logit-formula-generator
           negate probability    :{r_justed(clause_gen.literal_gen.negate_probability)}
           seed                  :{r_justed(seed)}
'''

    for line in cnf_header.split('\n'):
        if not line.strip():
            print()
            continue
        if line.strip() == '-' * 76:
            print(f'{comment_sign}{line}')
            continue
        print(f'{comment_sign} {line}')


def _k_sat_number_of_clauses_type_check(argument: str) -> Tuple[int, int]:
    if ',' in argument:
        k, number_of_clauses = argument.split(',')
        k = int(k), int(number_of_clauses)
    else:
        k = int(argument)
        k = k, None
    if k[0] < 1:
        raise argparse.ArgumentTypeError(f'in k-SAT the \'k\' can not be less than 1, not {k[0]}')
    return k


def _k_sat_propability_type_check(argument: str) -> Tuple[int, float]:
    """type check for parser: integer,float, example 1,0.7
    integer > 0, 0 <= float <= 1
    CNF k-SAT number can be provided with probability after coma
    There can be no whitespace between integer and float. Only coma is allowed
    """
    if ',' in argument:
        k, probability = argument.split(',')
        k = int(k), float(probability)
    else:
        k = int(argument), None
    if k[0] < 1:
        raise argparse.ArgumentTypeError(f'in k-SAT the \'k\' can not be less than 1, not {k[0]}')
    if k[1] is not None and (k[1] > 1 or k[1] < 0):
        raise argparse.ArgumentTypeError(f'the probability must be between 0 and 1, not {k[1]}')
    return k


def _literal_to_clause_ratio(argument: str) -> Tuple[float, float]:
    """:return how many literals there are in one clause."""
    if ':' not in argument:
        raise argparse.ArgumentTypeError('ratio must contain \':\'')
    literals, clauses = argument.split(':')
    return float(literals), float(clauses)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Script for generating SAT formulas')
    parser.set_defaults(parser_used='general')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=version,
                        help='prints current version')
    parser.add_argument('-s', '--seed',
                        type=int,
                        help='makes generator repeatable')
    parser.add_argument('-o', '--output-file',
                        help='output to file instead stdout')
    parser.add_argument('-F', '--output-format',
                        default='tptp',
                        choices=['tptp', 'dimacs'],
                        help='provide output in desired syntax')

    subparsers = parser.add_subparsers(description='available generators types')
    cnf_parser = subparsers.add_parser('cnf',
                                       description='generate formula in cnf format. ')
    cnf_parser.set_defaults(parser_used='cnf')
    cnf_parser.add_argument('-l', '--literals',
                            type=int,
                            help='how many variables to generate. If -c/--clauses nor -l/--variables-to-clauses-ratio is provided, '
                                 'ratio literals:clauses defaults to 2:1')
    cnf_parser.add_argument('-u', '--unique-literals',
                            type=int,
                            help='how many different literals to produce. Defaults to --literals')
    cnf_parser.add_argument('-c', '--clauses',
                            type=int,
                            help='how many clauses to generate. If -l/--literals nor -r/--variables-to-clauses-ratio is provided, '
                                 'ratio literals:clauses defaults to 2:1')
    cnf_parser.add_argument('-m', '--max-variables-per-clause',
                            type=int,
                            help='maximum clause length. Defaults to literals/clauses')
    cnf_parser.add_argument('-n', '--negate-probability',
                            type=float,
                            help='probability, that literal will be negative. Default 0.5')
    cnf_parser.add_argument('-r', '--variables-to-clauses-ratio',
                            type=_literal_to_clause_ratio,
                            help='in format \'float:float\'. 2.5:1 means there are 2.5 variables per 1 clause (rounded down to int). '
                                 'Combine with -l/--literals or -c/--clauses to get precise number of variables')

    k_sat_parser = subparsers.add_parser('k-sat',
                                         description='generate k-SAT formula or any combination of k-SAT formulas')
    k_sat_parser.set_defaults(parser_used='k-sat')

    # group = k_sat_parser.add_mutually_exclusive_group()
    k_sat_parser.add_argument('-c', '--clauses',
                              type=int,
                              help='how many clauses to generate. Use only with -k option. Note that number of clauses will '
                                   'be met, at the cost of different probability')
    # group.add_argument('-l', '--literals',
    #                    type=int,
    #                    help='how many variables to generate. Use only with -k option')
    k_sat_parser.add_argument('-n', '--negate-probability',
                              type=float,
                              help='probability, that literal will be negative. Default 0.5')
    k_sat_parser.add_argument('-u', '--unique-literals',
                              type=int,
                              help='how many different literals to produce. Defaults to --literals')

    group = k_sat_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-k', '--k-probability',
                       type=_k_sat_propability_type_check,
                       metavar='K,PROBABILITY',
                       nargs='+',
                       help='generate only CNF in k-SAT. Pass list of allowed k values. '
                            'probabilities must sum up to 1. Leave probability empty to calculate automatically'
                            'Ex. -k 1 3 - generate CNF formula that has 50%% 1-SAT and 50%% 3-SAT, '
                            '-k 4 5 6 7 - formula has 25%% of 4-,5-,6-,7-SAT, '
                            '-k 1,0.7 3 - formula has 70%% of 1-SAT, 30%% 3-SAT, '
                            '-k 4,0.1 5,0.6 6 7 - formula has 10%% of 4-SAT, 60%% of 5-SAT, 15%% of 6-SAT, 15%% of 7-SAT')
    group.add_argument('-k-n', '--k-number-of-clauses',
                       metavar='K,NUMBER_OF_CLAUSES',
                       type=_k_sat_number_of_clauses_type_check,
                       nargs='+',
                       help='same as -k, but instead of probability, use fixed numbers'
                            'Leave NUMBER_OF_CLAUSES empty to calculate automatically from -c/--clauses'
                            '-k 1,5 3 - formula has 5 1-SAT clauses, -c/--clauses - 5  3-SAT clauses'
                            '-k 1,5 3,6 - formula has 5 1-SAT clauses, 6 3-SAT clauses. Use of -c/--clauses is prohibited now')

    args = parser.parse_args()

    # common options
    if args.seed is None:
        args.seed = int(time.time() * 1000)
    random.seed(int(args.seed))

    if args.output_file is not None:
        sys.stdout = open(args.output_file, 'w')

    if args.parser_used == 'general':
        parser.print_help()
        sys.exit(1)
    elif args.parser_used == 'cnf':

        # cnf subparser
        if args.variables_to_clauses_ratio is not None:
            ratio = args.variables_to_clauses_ratio[0] / args.variables_to_clauses_ratio[1]
            if ratio < 1:
                cnf_parser.error(f'literals to clause ratio must be greater than 1, now is {ratio}')

            if args.literals is not None and args.clauses is not None:
                cnf_parser.error('when defining ratio, it does not make sense to use both --literals and --clauses')
            elif args.clauses is None:
                args.clauses = int(args.literals / ratio)
            elif args.literals is None:
                args.literals = int(args.clauses * ratio)
            else:
                assert False, bug_message
        elif args.clauses is not None and args.literals is None:
            args.literals = int(args.clauses * 2)
        elif args.clauses is None and args.literals is not None:
            args.clauses = int(args.literals / 2)
        elif args.clauses is None and args.literals is None:
            cnf_parser.error('provide either --literals or --clauses')
        elif args.clauses is not None and args.literals is not None:
            if args.literals < args.clauses:
                cnf_parser.error('there must be at least one literal per clause')
        else:
            assert False, bug_message

        if args.max_variables_per_clause is None:
            args.max_variables_per_clause = ceil(args.literals / args.clauses)

        if args.negate_probability is not None:
            if not 0 <= args.negate_probability <= 1:
                cnf_parser.error('probability range is [0.0, 1.0]')
        else:
            args.negate_probability = 0.5

        if args.unique_literals is not None:
            if args.literals < args.unique_literals:
                cnf_parser.error('number of unique literals must be smaller or equal to literals')
        else:
            args.unique_literals = args.literals

    elif args.parser_used == 'k-sat':
        k_clauses = {}
        if args.k_probability is not None:
            if args.clauses is None:
                k_sat_parser.error('provide how many clauses to generate with -c')
            # todo check for duplicate k

            P = sum(p for k, p in args.k_probability if p is not None)
            if P > 1:
                k_sat_parser.error('sum of probabilities is bigger than 1')

            number_of_k_with_none_probability = len([_ for _, p in args.k_probability if p is None])
            for i, (k, p) in enumerate(args.k_probability):
                if p is None:
                    args.k_probability[i] = k, (1 - P) / number_of_k_with_none_probability

            if sum(p for k, p in args.k_probability) != 1:
                k_sat_parser.error('probability must sum up to 1')
            if any(p < 0 for k, p in args.k_probability):
                k_sat_parser.error('negative probability detected')
            if any(p == 0 for k, p in args.k_probability):
                k_sat_parser.error('probability equal to 0 is pointless')
            if any(p == 1 for k, p in args.k_probability) and len(args.k_probability) > 1:
                k_sat_parser.error('one element has probability of 1. The rest has probability of 0')

            clauses_left = args.clauses
            for k, p in args.k_probability:
                number_of_k_sat = int(args.clauses * p)
                clauses_left -= number_of_k_sat
                if number_of_k_sat == 0:
                    print(f'WARNING: none {k}-SAT formula will be generated. Increase -c/--clauses or probability')
                else:
                    k_clauses[k] = number_of_k_sat

            # make sure all clauses are distributed
            if clauses_left != 0:
                args.k_probability = sorted(args.k_probability, key=lambda k_p: k_p[1])
                i = 0
                while clauses_left != 0:
                    k = args.k_probability[i][0]
                    k_clauses[k] += 1
                    clauses_left -= 1
                    i += 1
                    i %= len(args.k_probability)

        elif args.k_number_of_clauses is not None:
            if not any(n is None for k, n in args.k_number_of_clauses):
                if args.clauses is not None:
                    k_sat_parser.error('do not provide -c/--clauses, when all of k-SAT number of occurrences '
                                       'is provided in -k-n')
            else:
                if args.clauses is None:
                    k_sat_parser.error('provide total number of clauses with -c/--clauses, so that I can compute '
                                       'missing k-SAT number of occurrences')

                clauses_left = args.clauses - sum(n for k, n in args.k_number_of_clauses if n is not None)
                number_of_k_with_none_n = len([k for k, n in args.k_number_of_clauses if n is None])
                if number_of_k_with_none_n != 0:
                    average_calauses_per_none_n = int(clauses_left / number_of_k_with_none_n)
                    # args.k_number_of_clauses = []  # todo
                    for i, (k, n) in enumerate(args.k_number_of_clauses):
                        if n is None:
                            args.k_number_of_clauses[i] = k, average_calauses_per_none_n
                            clauses_left -= average_calauses_per_none_n

                # make sure all clauses are distributed
                if clauses_left != 0:
                    args.k_number_of_clauses = sorted(args.k_number_of_clauses, key=lambda k_n: k_n[1])
                    i = 0
                    while clauses_left != 0:
                        k = args.k_number_of_clauses[i][0]
                        k_clauses[k] += 1
                        clauses_left -= 1
                        i += 1
                        i %= len(args.k_number_of_clauses)

            for k, n in args.k_number_of_clauses:
                k_clauses[k] = n

        args.k_clauses = k_clauses

    return args


if __name__ == '__main__':
    args = parse_args()

    clause_gen = None
    if args.parser_used == 'cnf':
        lit_gen_init = {}
        clause_gen_init = {}
        if args.literals is not None:
            lit_gen_init['total_literals'] = args.literals
        if args.unique_literals is not None:
            lit_gen_init['unique_literals'] = args.unique_literals
        if args.negate_probability is not None:
            lit_gen_init['negate_probability'] = args.negate_probability

        clause_gen_init['total_clauses'] = args.clauses

        lit_gen = RandomLiteralGenerator(**lit_gen_init)
        clause_gen = KSATClauseGenerator(literal_gen=lit_gen, k_clauses='random', **clause_gen_init)

    elif args.parser_used == 'k-sat':
        lit_gen_init = {}
        clause_gen_init = {}
        if args.unique_literals is not None:
            lit_gen_init['unique_literals'] = args.unique_literals
        if args.negate_probability is not None:
            lit_gen_init['negate_probability'] = args.negate_probability

        clause_gen_init['k_clauses'] = args.k_clauses

        lit_gen = RandomLiteralGenerator(**lit_gen_init)
        clause_gen = KSATClauseGenerator(literal_gen=lit_gen, **clause_gen_init)
    else:
        assert False, bug_message

    if args.output_format == 'tptp':
        print_header(lit_gen=clause_gen.literal_gen, clause_gen=clause_gen, output_file=args.output_file,
                     comment_sign='%', seed=args.seed)
        for i in clause_gen:
            print(i.to_tptp())
    elif args.output_format == 'dimacs':
        print_header(lit_gen=clause_gen.literal_gen, clause_gen=clause_gen, output_file=args.output_file,
                     comment_sign='c', seed=args.seed)
        print(f"p {clause_gen.total_clauses} {clause_gen.literal_gen.total_literals}")
        for i in clause_gen:
            print(i.to_dimacs())
