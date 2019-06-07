import argparse
import sys
from collections import namedtuple
from typing import Tuple

from src.clause import LiteralGenerator, VariableLengthClauseGenerator

k_sat_propability = namedtuple('k_SAT_number', ['k', 'propability'])
k_sat_number_of_clauses = namedtuple('k_SAT_number', ['k', 'number_of_clauses'])


def _k_sat_number_of_clauses_type_check(argument: str) -> k_sat_number_of_clauses:
    if ',' in argument:
        k, number_of_clauses = argument.split(',')
        k = k_sat_number_of_clauses(int(k), int(number_of_clauses))
    else:
        k = int(argument)
        k = k_sat_number_of_clauses(k, None)
    if k.k < 1:
        raise argparse.ArgumentTypeError(f'in k-SAT the \'k\' can not be less than 1, not {k.k}')
    return k


def _k_sat_propability_type_check(argument: str) -> k_sat_propability:
    """type check for parser: integer,float, example 1,0.7
    integer > 0, 0 <= float <= 1
    CNF k-SAT number can be provided with probability after coma
    There can be no whitespace between integer and float. Only coma is allowed
    """
    if ',' in argument:
        k, probability = argument.split(',')
        k = k_sat_propability(int(k), float(probability))
    else:
        k = int(argument)
        k = k_sat_propability(k, None)
    if k.k < 1:
        raise argparse.ArgumentTypeError(f'in k-SAT the \'k\' can not be less than 1, not {k.k}')
    if k.propability is not None and (k.propability > 1 or k.propability < 0):
        raise argparse.ArgumentTypeError(f'the probability must be between 0 and 1, not {k.propability}')
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
                        version='Pre-alpha 0.1',
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
                            help='maximum clause length. Defaults to 2 * literals/clauses')
    cnf_parser.add_argument('-n', '--negate-probability',
                            type=float,
                            help='propability, that literal will be negative. Default 0.5')
    cnf_parser.add_argument('-r', '--variables-to-clauses-ratio',
                            type=_literal_to_clause_ratio,
                            help='in format \'float:float\'. 2.5:1 means there are 2.5 variables per 1 clause (rounded down to int). '
                                 'Combine with -l/--literals or -c/--clauses to get precise number of variables'
                                 '')

    k_sat_parser = subparsers.add_parser('k-sat',
                                         description='generate k-SAT formula or any combination of k-SAT formulas')
    k_sat_parser.set_defaults(parser_used='k-sat')

    group = k_sat_parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--clauses',
                       type=int,
                       help='how many clauses to generate')
    group.add_argument('-l', '--literals',
                       type=int,
                       help='how many variables to generate')
    k_sat_parser.add_argument('-u', '--unique-literals',
                              type=int,
                              help='how many different literals to produce. Defaults to --literals')

    group = k_sat_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-k',
                       type=_k_sat_propability_type_check,
                       metavar='K,Probability',
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
    if args.parser_used == 'general':
        parser.print_help()
        sys.exit(1)
    elif args.parser_used == 'cnf':
        # generator parser
        if args.seed is not None:
            raise NotImplementedError()

        if args.output_file is not None:
            raise NotImplementedError()

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
                assert False, 'this shouldn\'t happen. This is bug'

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
            assert False, 'this shouldn\'t happen. This is bug'

        args.max_variables_per_clause = args.literals // args.clauses * 2 if args.max_variables_per_clause is None else args.max_variables_per_clause
        if args.negate_probability is not None:
            if not 0 <= args.negate_probability <= 1:
                parser.error('probability range is [0.0, 1.0]')
        else:
            args.negate_probability = 0.5

        if args.unique_literals is not None:
            if args.literals < args.unique_literals:
                cnf_parser.error('number of unique literals must be smaller or equal to literals')
        else:
            args.unique_literals = args.literals



    elif args.parser_used == 'k-sat':
        raise NotImplementedError()

    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    if args.parser_used == 'cnf':
        var_gen_input = {}
        clause_gen_input = {}
        if args.literals is not None:
            var_gen_input['total_literals'] = args.literals
        # if args.literal_prefix is not None:
        #     var_gen_input['name'] = args.literal_prefix
        if args.unique_literals is not None:
            var_gen_input['unique_literals'] = args.unique_literals
        if args.negate_probability is not None:
            var_gen_input['negate_probability'] = args.negate_probability

        clause_gen_input['total_clauses'] = args.clauses

        lit_gen = LiteralGenerator(**var_gen_input)
        clause_gen = VariableLengthClauseGenerator(literal_gen=lit_gen, **clause_gen_input)
        if args.output_format == 'tptp':
            for i in clause_gen:
                print(i.to_tptp())
        elif args.format == 'dimacs':
            print(f"p {clause_gen.total_clauses} {clause_gen.literal_gen.total_literals}")
            for i in clause_gen:
                print(i.to_dimacs())

    # c = KSATClauseGenerator(
    #     k_clauses={1: 1, 2: 1, 4: 4}
    # )
