from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo:
    number_of_variables: int = 0
    number_of_clauses: int = 0
    max_clause_size: int = 0
    clause_sizes: Dict[int, int] = field(default_factory=dict)
    """Dict[clause_size, number_of_clauses]"""
    repeated_variables: [Dict, int] = field(default_factory=dict)
    """Dict[variable_name, number_of_repetitions in formula"""
    number_of_variables_with_always_connectives: int = 0
    number_of_variables_with_eventually_connectives: int = 0
    number_of_variables_without_connective: int = 0
    number_of_negated_variables: int = 0
