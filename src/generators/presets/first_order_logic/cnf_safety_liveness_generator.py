from typing import Iterable

import src.generators.syntax_tree_generators.first_order_logic as fol_gen
from src.ast.first_order_logic import CNFFormula
from src.generators import AstGenerator
from src.generators.contraint_solver.first_order_logic.z3_solver import Z3CNFConstraintSolver
from src.generators.utils import IntegerRange


class CNFSafetyLivenessGenerator(AstGenerator):
    def __init__(self, functor_arity: Iterable[int], functor_recursion_depth: int, predicate_arities: Iterable[int],
                 atom_connectives: Iterable[str], clause_lengths: Iterable[int], number_of_clauses: IntegerRange,
                 number_of_literals: IntegerRange, literal_negation_chance: float, predicate_names: Iterable[str],
                 functor_names: Iterable[str], variable_names: Iterable[str]):
        self.literal_negation_chance = literal_negation_chance
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

    def generate(self) -> CNFFormula:
        v = fol_gen.VariableGenerator(variable_names=self.variable_names)
        f = fol_gen.FunctorGenerator(variable_gen=v, arities=self.functor_arity,
                                     functor_names=self.functor_names,
                                     max_recursion_depth=self.functor_recursion_depth)
        p = fol_gen.SafetyLivenessPredicateGenerator(variable_gen=v, arities=self.predicate_arities,
                                                     predicate_names=self.predicate_names, functor_gen=f)
        a = fol_gen.AtomGenerator(variable_gen=v, connectives=self.atom_connectives, predicate_gen=p)
        l = fol_gen.LiteralGenerator(negation_chance=self.literal_negation_chance, atom_gen=a)

        solver = Z3CNFConstraintSolver(clause_lengths=self.clause_lengths, number_of_clauses=self.number_of_clauses,
                                       number_of_literals=self.number_of_literals)
        for solution in solver.solve_in_random_order():
            clause_gens = {}
            for clause_len, amount_of_clauses in solution.items():
                c = fol_gen.CNFClauseGenerator(clause_lengths={clause_len}, literal_gen=l)
                clause_gens[c] = amount_of_clauses
            F = fol_gen.CNFFormulaGenerator(clause_gens=clause_gens)
            yield F.generate()
