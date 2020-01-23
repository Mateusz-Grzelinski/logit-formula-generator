from __future__ import annotations

import random
from typing import Iterable

import src.syntax_tree.first_order_logic as fol
from src.generators import SyntaxTreeGenerator
from src.syntax_tree import LogicalConnective
from .atom_generator import AtomGenerator


class FormulaGenerator(SyntaxTreeGenerator):
    def __init__(self, atoms_gen: AtomGenerator, number_of_atoms: int, number_of_existential_quantifiers: int,
                 number_of_universal_quantifiers: int, quantifier_number_of_atoms: Iterable[int]) -> None:
        self.atoms_gen = atoms_gen
        self.number_of_atoms = number_of_atoms
        self.number_of_existential_quantifiers = number_of_existential_quantifiers
        self.number_of_universal_quantifiers = number_of_universal_quantifiers
        self.quantifier_max_number_of_atoms = quantifier_number_of_atoms
        assert number_of_existential_quantifiers + number_of_universal_quantifiers < number_of_atoms
        assert number_of_universal_quantifiers == 0, 'currently not supported'
        assert number_of_existential_quantifiers == 0, 'currently not supported'
        assert not quantifier_number_of_atoms, 'currently not suppported'

    def generate(self) -> fol.FOLFormula:
        return self._atom_only_formula_gen(atom_gen=self.atoms_gen, number_of_atoms=self.number_of_atoms)

    def _atom_only_formula_gen(self, atom_gen: AtomGenerator, number_of_atoms: int) -> fol.FOLFormula:
        """Recursive generation in python is not a good idea"""
        # todo randomize logical connective
        assert number_of_atoms != 0
        if number_of_atoms == 1:
            return fol.FOLFormula(children=[atom_gen.generate()], binary_logical_connective=LogicalConnective.OR)
        elif number_of_atoms == 2:
            return fol.FOLFormula(children=[atom_gen.generate(), atom_gen.generate()],
                                  binary_logical_connective=LogicalConnective.OR)
        else:
            left_subtree_size = random.randrange(1, number_of_atoms)
            right_subtree_size = number_of_atoms - left_subtree_size
            left_subtree = self._atom_only_formula_gen(atom_gen, number_of_atoms=left_subtree_size)
            right_subtree = self._atom_only_formula_gen(atom_gen, number_of_atoms=right_subtree_size)
            return fol.FOLFormula(children=[left_subtree, right_subtree],
                                  binary_logical_connective=LogicalConnective.OR)
