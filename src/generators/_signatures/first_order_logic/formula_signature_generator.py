from __future__ import annotations

import random
from typing import Any, Generator, Iterable

import src.ast.first_order_logic as fol
from src.ast import LogicalConnective
from src.generators import AstGenerator
from .atom_signature_generator import AtomSignatureGenerator


def _atom_only_folmula_gen(atom_gen: AtomSignatureGenerator, number_of_atoms: int) -> fol.Formula:
    assert number_of_atoms != 0
    if number_of_atoms == 1:
        for atom in atom_gen.generate():
            yield fol.Formula(items=[atom], logical_connective=LogicalConnective.OR)
    elif number_of_atoms == 2:
        for atom_left in atom_gen.generate():
            for atom_right in atom_gen.generate():
                yield fol.Formula(items=[atom_left, atom_right], logical_connective=LogicalConnective.OR)
    else:
        sizes = list(range(1, number_of_atoms))  # or number_of_atoms // 2
        random.shuffle(sizes)
        for left_subtree_size in sizes:
            right_subtree_size = number_of_atoms - left_subtree_size
            for left_subtree in _atom_only_folmula_gen(atom_gen, number_of_atoms=left_subtree_size):
                for right_subtree in _atom_only_folmula_gen(atom_gen, number_of_atoms=right_subtree_size):
                    yield fol.Formula(items=[left_subtree, right_subtree], logical_connective=LogicalConnective.OR)


class FormulaSignatureGenerator(AstGenerator):
    def __init__(self, atoms_gen: AtomSignatureGenerator, number_of_atoms: int,
                 number_of_existential_quantifiers: int,
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

    def generate(self) -> Generator[fol.Quantifier, Any, Any]:
        yield _atom_only_folmula_gen(atom_gen=self.atoms_gen, number_of_atoms=self.number_of_atoms)
