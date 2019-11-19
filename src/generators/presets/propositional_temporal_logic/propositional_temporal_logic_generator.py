from collections import Iterable
from typing import Generator, Any

import src.ast.propositional_temporal_logic as ptl
import src.generators._signatures.propositional_temporal_logic as ptl_signatures
from src.generators import AstGenerator
from ..._post_processors.propositional_temporal_logic_post_procesor import \
    PropositionalTemporalLogicPostProcessor


class PropositionalTemporalLogicGenerator(AstGenerator):
    variable_name = 'v'

    def __init__(self, variable_names: Iterable[str], number_of_variables_without_connective: int,
                 number_of_variables_with_always_connectives: int,
                 number_of_variables_with_eventually_connectives: int,
                 number_of_variables_with_both_connectives: int) -> None:
        self.variable_names = set(variable_names)
        self.number_of_variables_with_both_connectives = number_of_variables_with_both_connectives
        self.number_of_variables_with_eventually_connectives = number_of_variables_with_eventually_connectives
        self.number_of_variables_with_always_connectives = number_of_variables_with_always_connectives
        self.number_of_variables_without_connective = number_of_variables_without_connective

    def generate(self) -> Generator[ptl.Formula, Any, Any]:
        formula_signature = ptl_signatures.FormulaSignatureGenerator(number_of_variables=self.number_of_variables)
        post_processor = PropositionalTemporalLogicPostProcessor(
            variable_names=self.variable_names,
            number_of_variables_with_both_connectives=self.number_of_variables_with_both_connectives,
            number_of_variables_with_always_connectives=self.number_of_variables_with_always_connectives,
            number_of_variables_with_eventually_connectives=self.number_of_variables_with_eventually_connectives,
            number_of_variables_without_connective=self.number_of_variables_without_connective
        )
        for formula in formula_signature.generate():
            post_processor.post_process(formula=formula)
            yield formula

    @property
    def number_of_variables(self):
        return sum([self.number_of_variables_without_connective,
                    self.number_of_variables_with_always_connectives,
                    self.number_of_variables_with_eventually_connectives,
                    self.number_of_variables_with_both_connectives])
