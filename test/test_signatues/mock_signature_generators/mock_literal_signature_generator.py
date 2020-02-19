from logic_formula_generator.generators._signatures.first_order_logic import LiteralGenerator

from logic_formula_generator.syntax_tree.first_order_logic import Literal
from test.test_signatues.mock_signature_generators.mock_atom_signature_generator import atom0, atom1, atom0_1


class MockLiteralGenerator(LiteralGenerator):
    def __init__(self):
        super().__init__(atom_gen=None)

    def generate(self):
        global literal0, literal1, literal1_neg, literal0_1
        yield literal0
        yield literal1
        yield literal1_neg
        yield literal0_1


literal0 = Literal(children=atom0, negated=False)
literal1 = Literal(children=atom1, negated=False)
literal1_neg = Literal(children=atom1, negated=True)
literal0_1 = Literal(children=atom0_1, negated=False)
