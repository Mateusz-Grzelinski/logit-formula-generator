# Logic formula generator

This is random formula generator for various logical systems. Generated are used to measure performance of SAT/SMT solvers. Currently user can generate:
- first order logic: `examples/first_order_logic` in TPTP format
    - in CNF (conjuctive normal form) - completed
    - full FOL (with quantifiers and more logical connectives) - in progress
- propositional temporal logic: `examples/temporal_logic` in format required by solver Inkresat 

This repository is implementation of bachelor thesis "System of random generation of logical formulas for first order logic" by Mateusz Grzeliński, but also explores other areas.

## TODO's

- implement full FOL formula generator
- implement incremental benhcmark generation
- streamline fomula generation, benchmarking and analyzing
- add tests

## Run

See `examples/*`

## Related

- some documentation and thesis: https://github.com/Przemcom/studio_projektowe1
- tool used to benchmark solvers: https://github.com/Przemcom/proversBenchmark 
- TPTP format and benchmark library: http://tptp.org/
