from src.lfg import VariableGenerator, ClauseGenerator

if __name__ == '__main__':
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

