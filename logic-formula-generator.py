import argparse
from collections import namedtuple

from src.clause import LiteralGenerator, VariableLengthClauseGenerator, KSATClauseGenerator

k_sat_propability = namedtuple('k_SAT_number', ['k', 'propability'])
k_sat_number_of_clauses = namedtuple('k_SAT_number', ['k', 'number_of_clauses'])


def k_sat_number_of_clauses_type_check(argument: str) -> k_sat_number_of_clauses:
    if ',' in argument:
        k, number_of_clauses = argument.split(',')
        k = k_sat_number_of_clauses(int(k), int(number_of_clauses))
    else:
        k = int(argument)
        k = k_sat_number_of_clauses(k, None)
    if k.k < 1:
        raise argparse.ArgumentTypeError(f'in k-SAT the \'k\' can not be less than 1, not {k.k}')
    return k


def k_sat_propability_type_check(argument: str) -> k_sat_propability:
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


def float_colon_float(argument: str) -> float:
    """:return how many literals there are in one clause."""
    if ':' not in argument:
        raise argparse.ArgumentTypeError('ratio must contain \':\'')
    literal, clause = argument.split(':')
    ratio = float(literal) / float(clause)
    if ratio < 1:
        raise argparse.ArgumentError('there must be at least one literal per clause')

    return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Script for generating SAT formulas')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s Pre-alpha 0.1',
                        help='Prints current version')
    parser.add_argument('-s', '--seed',
                        type=int)
    parser.set_defaults(parser_used='general')

    subparsers = parser.add_subparsers(description='available generators types')
    cnf_parser = subparsers.add_parser('cnf',
                                       description='generate formula in cnf format')
    cnf_parser.set_defaults(parser_used='cnf')
    cnf_parser.add_argument('-l', '--literals',
                            type=int,
                            help='how many variables to generate')
    cnf_parser.add_argument('-u', '--unique-literals',
                            type=int,
                            help='')
    cnf_parser.add_argument('-c', '--clauses',
                            type=int,
                            help='how many clauses to generate')
    cnf_parser.add_argument('-m', '--max-variables-per-clause',
                            type=int)
    cnf_parser.add_argument('-n', '--negate-probability',
                            type=float,
                            default=0.5,
                            help='propability, that literal will be negative')
    cnf_parser.add_argument('-r', '--variables-to-clauses-ratio',
                            type=float_colon_float)

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
                              help='')

    group = k_sat_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-k',
                       type=k_sat_propability_type_check,
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
                       type=k_sat_number_of_clauses_type_check,
                       nargs='+',
                       help='same as -k, but instead of probability, use fixed numbers'
                            'Leave NUMBER_OF_CLAUSES empty to calculate automatically from --clauses'
                            '-k 1,5 3 - formula has 5 1-SAT clauses, --clauses - 5  3-SAT clauses'
                            '-k 1,5 3,6 - formula has 5 1-SAT clauses, 6 3-SAT clauses. Use of --clauses is prohibited now')

    args = parser.parse_args()
    if args.parser_used == 'cnf':
        if args.variables_to_clauses_ratio is not None:
            if args.literals is None and args.clauses is None:
                cnf_parser.error('when defining ratio, provide either --literals or --clauses')
            if args.literals is not None and args.clauses is not None:
                cnf_parser.error('when defining ratio, it does not make sense to use both --literals and --clauses')

        if args.literals is not None and args.clauses is not None and args.literals < args.clauses:
            cnf_parser.error('there must be at least one literal per clause')

        if args.unique_literals is not None and args.literals is not None and args.literals < args.unique_literals:
            cnf_parser.error('number of unique literals must be smaller or equal to literals')
    elif args.parser_used == 'k-sat':
        raise Exception('k-sat is not implemented yet')

    return args


if __name__ == '__main__':
    args = parse_args()

    # c = VariableLengthClauseGenerator(
    #                                   total_clauses=10,
    #                                   )
    c = KSATClauseGenerator(
                            k_clauses={1: 1, 2: 1, 4:4}
                            )
    print(f"p {c.total_clauses} {c.literal_gen.total_literals}")
    for i in c:
        print(i.to_tptp())
