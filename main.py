import argparse

from src.lfg import VariableGenerator, ClauseGenerator


def parse_args():
    parser = argparse.ArgumentParser(prog="Logic formula generator",
                                     description="Script for generating SAT formulas")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s Pre-alpha 0.1",
                        help="Prints current version")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    clauses = 10
    v = VariableGenerator(name="a",
                          unique_variables=5,
                          total_variables=200,
                          negate_probability=0.1)
    c = ClauseGenerator(variable_gen=v,
                        total_clauses=10,
                        )
    print(f"p {c.total_clauses} {v.total_variables}")
    # print(c.new_clause.to_dimacs())
    for i in range(clauses):
        print(c.new_clause.to_dimacs())
