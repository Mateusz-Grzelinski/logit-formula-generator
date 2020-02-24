from typing import Iterable, Union, Generator

import logic_formula_generator.generators.syntax_tree_generators.first_order_logic as fol_gen
import logic_formula_generator.syntax_tree.first_order_logic as fol
from logic_formula_generator.generators import SyntaxTreeGenerator
from logic_formula_generator.generators.contraint_solver.first_order_logic.z3_solver import Z3CNFConstraintSolver
from logic_formula_generator.generators.utils import IntegerRange
from logic_formula_generator.syntax_tree import LogicalConnective


class CNFSafetyLivenessPreset(SyntaxTreeGenerator):
    def __init__(self, functor_arity: Iterable[int], functor_recursion_depth: int, predicate_arities: Iterable[int],
                 atom_connectives: Iterable[Union[None, str]], clause_lengths: Iterable[int],
                 number_of_clauses: IntegerRange, number_of_literals: IntegerRange, literal_negation_chance: float,
                 predicate_names: Iterable[str], functor_names: Iterable[str],
                 variable_names: Iterable[str]):
        self.atom_connectives = atom_connectives
        self.literal_negation_chance = literal_negation_chance
        self.predicate_names = predicate_names
        self.functor_names = functor_names
        self.functor_recursion_depth = functor_recursion_depth
        self.variable_names = variable_names
        self.number_of_literals = number_of_literals
        self.number_of_clauses = number_of_clauses
        self.clause_lengths = clause_lengths
        self.predicate_arities = predicate_arities
        self.functor_arity = functor_arity

    def generate(self) -> Generator[fol.FirstOrderLogicFormula, None, None]:
        v = fol_gen.VariableGenerator(variable_names=self.variable_names)
        f = fol_gen.FunctorGenerator(variable_gen=v, arities=self.functor_arity,
                                     functor_names=self.functor_names,
                                     max_recursion_depth=self.functor_recursion_depth)
        p = fol_gen.PredicateSafetyLivenessGenerator(variable_gen=v, arities=self.predicate_arities,
                                                     predicate_names=self.predicate_names, functor_gen=f)
        a = fol_gen.AtomGenerator(math_connectives=self.atom_connectives, predicate_gen=p, variable_gen=v,
                                  functor_gen=f, negation_chance=self.literal_negation_chance)
        solver = Z3CNFConstraintSolver(clause_lengths=self.clause_lengths, number_of_clauses=self.number_of_clauses,
                                       number_of_literals=self.number_of_literals)
        for solution in solver.solve_in_random_order():
            root = fol.FirstOrderLogicFormula(children=[], binary_logical_connective=LogicalConnective.AND)
            for clause_len, amount_of_clauses in solution.items():
                for _ in range(amount_of_clauses):
                    clause = fol.FirstOrderLogicFormula(children=[], binary_logical_connective=LogicalConnective.OR)
                    for _ in range(clause_len):
                        clause.append(a.generate())
                    root.append(clause)
            yield root
