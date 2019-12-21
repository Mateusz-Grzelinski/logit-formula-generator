from typing import Iterable

import src.ast.first_order_logic as fol
import src.generators.syntax_tree_generators.first_order_logic as fol_gen
from ..._ast_generator import AstGenerator


class FormulaGenerator(AstGenerator):
    def __init__(self, functor_arity: Iterable[int], functor_recursion_depth: int, predicate_arities: Iterable[int],
                 atom_connectives: Iterable[str], number_of_atoms: int, number_of_universal_quantifiers: int,
                 number_of_existential_quantifiers: int, quantifier_number_of_atoms: Iterable[int],
                 predicate_names: Iterable[str], functor_names: Iterable[str],
                 variable_names: Iterable[str]):
        self.number_of_atoms = number_of_atoms
        self.predicate_names = predicate_names
        self.functor_names = functor_names
        self.functor_recursion_depth = functor_recursion_depth
        self.variable_names = variable_names
        self.number_of_universal_quantifiers = number_of_universal_quantifiers
        self.number_of_existential_quantifiers = number_of_existential_quantifiers
        self.quantifier_number_of_atoms = set(quantifier_number_of_atoms)
        self.atom_connectives = atom_connectives
        self.predicate_arities = predicate_arities
        self.functor_arity = functor_arity

    def generate(self) -> fol.FOLFormula:
        # todo add variable gen, fix arguments
        v = fol_gen.VariableGenerator(variable_names=self.variable_names)
        f = fol_gen.FunctorGenerator(arities=self.functor_arity, max_recursion_depth=self.functor_recursion_depth,
                                     variable_gen=v, functor_names=self.functor_names)
        p = fol_gen.PredicateGenerator(arities=self.predicate_arities, functor_gen=f, variable_gen=v,
                                       predicate_names=self.predicate_names)
        a = fol_gen.AtomGenerator(connectives=self.atom_connectives, predicate_gen=p, variable_gen=v)
        # q = fol_sig.QuantifierGenerator(atom_gen=a, number_of_atoms=)
        F = fol_gen.FormulaGenerator(atoms_gen=a, number_of_atoms=self.number_of_atoms,
                                     number_of_universal_quantifiers=self.number_of_universal_quantifiers,
                                     number_of_existential_quantifiers=self.number_of_existential_quantifiers,
                                     quantifier_number_of_atoms=self.quantifier_number_of_atoms)
        # add more constrains, similar to cnf generator
        return F.generate()
