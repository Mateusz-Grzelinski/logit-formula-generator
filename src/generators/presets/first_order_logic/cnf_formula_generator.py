import random
from random import randint
from typing import Iterable, Generator

import src.generators._signatures.first_order_logic as fol_sig
from src.ast.first_order_logic import CNFFormula
from src.generators import AstGenerator
from src.generators._contraint_solver.first_order_logic.z3_solver import Z3CNFConstraintSolver
from src.generators._post_processors.first_order_logic_post_processor import FOLPostProcessor
from src.generators.utils._range import IntegerRange


class CNFFormulaGenerator(AstGenerator):
    def __init__(self, functor_arity: Iterable[int], functor_recursion_depth: int, predicate_arities: Iterable[int],
                 atom_connectives: Iterable[str], clause_lengths: Iterable[int], number_of_clauses: IntegerRange,
                 number_of_literals: IntegerRange, predicate_names: Iterable[str], functor_names: Iterable[str],
                 variable_names: Iterable[str]):
        self.predicate_names = predicate_names
        self.functor_names = functor_names
        self.functor_recursion_depth = functor_recursion_depth
        self.variable_names = variable_names
        self.number_of_literals = number_of_literals
        self.number_of_clauses = number_of_clauses
        self.clause_lengths = clause_lengths
        self.atom_connectives = atom_connectives
        self.predicate_arities = predicate_arities
        self.functor_arity = functor_arity

    def generate(self) -> Generator[CNFFormula, None, None]:
        def new_formula_signatures(literal_gen) -> Generator[CNFFormula, None, None]:
            for solution in self.solve_constrains(allowed_clause_lengths=self.clause_lengths,
                                                  number_of_clauses=self.number_of_clauses,
                                                  number_of_literals=self.number_of_literals):
                clause_gens = {}
                for clause_len, amount_of_clauses in solution.items():
                    c = fol_sig.CNFClauseSignatureGenerator(clause_lengths={clause_len}, literal_gen=literal_gen)
                    clause_gens[c] = amount_of_clauses
                F = fol_sig.CNFFormulaSignatureGenerator(clause_gens=clause_gens)
                yield F.generate()

        post_proc = FOLPostProcessor(predicate_names=self.predicate_names, functor_names=self.functor_names,
                                     variable_names=self.variable_names)
        f = fol_sig.FunctorSignatureGenerator(arities=self.functor_arity,
                                              max_recursion_depth=self.functor_recursion_depth)
        p = fol_sig.PredicateSignatureGenerator(arities=self.predicate_arities, functor_gen=f)
        a = fol_sig.AtomSignatureGenerator(connectives=self.atom_connectives, predicate_gen=p)
        l = fol_sig.LiteralSignatureGenerator(atom_gen=a)

        formula_signature_generator = new_formula_signatures(literal_gen=l)
        skip_chance = random.random()
        cached_formula_generators = []
        more_signatures = True
        while cached_formula_generators or more_signatures:
            if cached_formula_generators and (not more_signatures or random.random() < skip_chance):
                index = randint(0, len(cached_formula_generators) - 1)
                try:
                    formula = next(cached_formula_generators[index])
                except StopIteration:
                    del cached_formula_generators[index]
                else:
                    post_proc.post_process(formula=formula)
                    yield formula
            else:
                try:
                    cached_formula_generators.append(next(formula_signature_generator))
                except StopIteration:
                    more_signatures = False

    @staticmethod
    def solve_constrains(allowed_clause_lengths: Iterable[int], number_of_clauses: IntegerRange,
                         number_of_literals: IntegerRange):
        solver = Z3CNFConstraintSolver(clause_lengths=allowed_clause_lengths, number_of_clauses=number_of_clauses,
                                       number_of_literals=number_of_literals)
        for solution in solver.solve_in_random_order():
            yield solution
