import random
from random import randint
from typing import Iterable, Generator

import src.ast.first_order_logic as fol
import src.generators._signatures.first_order_logic as fol_sig
from ..._ast_generator import AstGenerator
from ..._post_processors.first_order_logic_post_processor import FOLPostProcessor


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

    def generate(self) -> Generator[fol.Formula, None, None]:
        post_proc = FOLPostProcessor(predicate_names=self.predicate_names, functor_names=self.functor_names,
                                     variable_names=self.variable_names)
        f = fol_sig.FunctorSignatureGenerator(arities=self.functor_arity,
                                              max_recursion_depth=self.functor_recursion_depth)
        p = fol_sig.PredicateSignatureGenerator(arities=self.predicate_arities, functor_gen=f)
        a = fol_sig.AtomSignatureGenerator(connectives=self.atom_connectives, predicate_gen=p)
        # q = fol_sig.QuantifierSignatureGenerator(atom_gen=a, number_of_atoms=)
        F = fol_sig.FormulaSignatureGenerator(atoms_gen=a, number_of_atoms=self.number_of_atoms,
                                              number_of_universal_quantifiers=self.number_of_universal_quantifiers,
                                              number_of_existential_quantifiers=self.number_of_existential_quantifiers,
                                              quantifier_number_of_atoms=self.quantifier_number_of_atoms)

        formula_signature_generator = F.generate()
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
