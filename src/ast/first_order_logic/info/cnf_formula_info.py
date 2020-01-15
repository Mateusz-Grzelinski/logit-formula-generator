from dataclasses import dataclass, field
from typing import Dict

from src.ast.first_order_logic.conjunctive_normal_form._literal import Literal


@dataclass
class CNFFormulaInfo:
    number_of: Dict[str, int] = field(default_factory=dict)
    """Dict[FolElement, quantity], in mathematical sense"""
    # number_of_signatures: Dict[Type[FolElement], int] = field(default_factory=partial(defaultdict, int))
    # """Dict[FolElement, quantity], by element's signature (see bachelor thesis)"""
    number_of_instances: Dict[str, int] = field(default_factory=dict)
    """Dict[FolElement, quantity], every occurrence of element"""

    clause_lengths: Dict[int, int] = field(default_factory=dict)
    """Dict[clause_length, quantity]"""
    number_of_horn_clauses_instances: int = 0
    number_of_singleton_variables: int = 0

    number_of_negated_literal_instances: int = 0

    number_of_equality_atom_instances: int = 0

    predicate_arities: Dict[int, int] = field(default_factory=dict)
    """Dict[predicate_arity, quantity], counted by predicate instances"""

    functor_arities: Dict[int, int] = field(default_factory=dict)
    """Dict[functor_arity, quantity], counted by functor instances"""

    term_instances_depths: Dict[int, int] = field(default_factory=dict)
    """Dict[term_depth, quantity]"""

    @property
    def max_term_depth(self) -> int:
        return max(self.term_instances_depths.keys()) if self.term_instances_depths else 0

    @property
    def number_of_propositional_predicates(self) -> int:
        return self.predicate_arities[0]

    @property
    def number_of_constant_functors(self) -> int:
        return self.functor_arities[0]

    @property
    def number_of_positive_literal_instances(self) -> int:
        return self.number_of_instances[Literal] - self.number_of_negated_literal_instances

    @property
    def number_of_unit_clauses(self) -> int:
        return self.clause_lengths[1]

    @property
    def average_clause_size(self) -> float:
        return sum(length * quantity for length, quantity in self.clause_lengths.items()) / \
               sum(quantity for quantity in self.clause_lengths.values())

    @property
    def max_clause_size(self) -> int:
        return max(self.clause_lengths)
