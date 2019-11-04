from typing import Iterable, Generator

import src.generators._signatures.first_order_logic as fol
from src.ast.first_order_logic import CNFFormula
from src.generators import AstGenerator
from src.generators._contraint_solver.z3_solver import Z3ConstraintSolver
from src.generators._post_processors.fol_post_processor import FOLPostProcessor
from src.generators._range import IntegerRange


class CNFFormulaGenerator(AstGenerator):
    def __init__(self, functor_arity: Iterable[int], functor_recursion_depth: int, predicate_arities: Iterable[int],
                 connectives: Iterable[str], clause_lengths: Iterable[int], number_of_clauses: IntegerRange,
                 number_of_literals: IntegerRange, predicate_names: Iterable[str], functor_names: Iterable[str],
                 variable_names: Iterable[str]):
        self.predicate_names = predicate_names
        self.functor_names = functor_names
        self.functor_recursion_depth = functor_recursion_depth
        self.variable_names = variable_names
        self.number_of_literals = number_of_literals
        self.number_of_clauses = number_of_clauses
        self.clause_lengths = clause_lengths
        self.connectives = connectives
        self.predicate_arities = predicate_arities
        self.functor_arity = functor_arity

    def generate(self) -> Generator[CNFFormula, None, None]:
        post_proc = FOLPostProcessor(predicate_names=self.predicate_names, functor_names=self.functor_names,
                                     variable_names=self.variable_names)

        f = fol.FunctorSignatureGenerator(arities=self.functor_arity, max_recursion_depth=self.functor_recursion_depth)
        p = fol.PredicateSignatureGenerator(arities=self.predicate_arities, functor_gen=f)
        a = fol.AtomSignatureGenerator(allowed_connectives=self.connectives, predicate_gen=p)
        l = fol.LiteralSignatureGenerator(atom_gen=a)
        for solution in self.solve_constrains(allowed_clause_lengths=self.clause_lengths,
                                              number_of_clauses=self.number_of_clauses,
                                              number_of_literals=self.number_of_literals):
            clause_gens = {}
            for clause_len, amount_of_clauses in solution.items():
                c = fol.CNFClauseSignatureGenerator(clause_lengths={clause_len}, literal_gen=l)
                clause_gens[c] = amount_of_clauses
            F = fol.CNFFormulaSignatureGenerator(clause_gens=clause_gens)

            for formula in F.generate():
                post_proc.switch_names(formula=formula)
                yield formula

    @staticmethod
    def solve_constrains(allowed_clause_lengths: Iterable[int], number_of_clauses: IntegerRange,
                         number_of_literals: IntegerRange):
        solver = Z3ConstraintSolver(clause_lengths=allowed_clause_lengths, number_of_clauses=number_of_clauses,
                                    number_of_literals=number_of_literals)
        for solution in solver.solve_in_random_order():
            yield solution
