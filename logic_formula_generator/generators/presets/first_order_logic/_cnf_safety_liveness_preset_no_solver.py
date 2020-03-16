from typing import Iterable, Union, Sequence

import logic_formula_generator.generators.syntax_tree_generators.first_order_logic as fol_gen
import logic_formula_generator.generators.syntax_tree_generators.first_order_logic.normal_forms as fol_normal_form_gen
from logic_formula_generator.generators import SyntaxTreeGenerator
from logic_formula_generator.syntax_tree.first_order_logic import FirstOrderLogicFormula


class CNFSafetyLivenessPresetNoSolver(SyntaxTreeGenerator):
    def __init__(self, functor_arity: Iterable[int], functor_recursion_depth: int,
                 predicate_arities: Iterable[int], predicate_names: Iterable[str],
                 atom_connectives: Iterable[Union[str, None]],
                 clause_lengths: Sequence[int], clause_lengths_weights: Sequence[float],
                 functor_names: Iterable[str], variable_names: Iterable[str],
                 min_number_of_clauses: int, min_number_of_literals: int,
                 literal_negation_chance: float, safety_liveness_ratio: float = 0.5):
        """safety_liveness_ratio range [0, 1] - 0 means all predicates represent safety"""
        self.safety_liveness_ratio = safety_liveness_ratio
        self.literal_negation_chance = literal_negation_chance
        self.predicate_names = predicate_names
        self.functor_names = functor_names
        self.functor_recursion_depth = functor_recursion_depth
        self.variable_names = variable_names
        self.clause_lengths = clause_lengths
        self.clause_lengths_weights = clause_lengths_weights
        self.atom_connectives = atom_connectives
        self.predicate_arities = predicate_arities
        self.functor_arity = functor_arity

        self.min_number_of_literals = min_number_of_literals
        self.min_number_of_clauses = min_number_of_clauses

    def generate(self) -> FirstOrderLogicFormula:
        v = fol_gen.VariableGenerator(variable_names=self.variable_names)
        f = fol_gen.FunctorGenerator(variable_gen=v, arities=self.functor_arity,
                                     functor_names=self.functor_names,
                                     max_recursion_depth=self.functor_recursion_depth)
        p = fol_gen.PredicateSafetyLivenessGenerator(variable_gen=v, arities=self.predicate_arities,
                                                     predicate_names=self.predicate_names, functor_gen=f,
                                                     safety_liveness_ratio=self.safety_liveness_ratio)
        a = fol_gen.AtomSafetyLivenessGenerator(predicate_gen=p)
        F = fol_normal_form_gen.CNFFormulaGeneratorSafetyLiveness(
            atom_gen=a, clause_lengths=self.clause_lengths, clause_lengths_weights=self.clause_lengths_weights,
            min_number_of_clauses=self.min_number_of_clauses, min_number_of_literals=self.min_number_of_literals,
            negation_probability=self.literal_negation_chance, safety_liveness_ratio=self.safety_liveness_ratio
        )
        return F.generate()
