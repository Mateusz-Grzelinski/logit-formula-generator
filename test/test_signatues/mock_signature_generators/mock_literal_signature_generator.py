from src.ast.first_order_logic import Literal

from src.generators._signatures.first_order_logic import LiteralSignatureGenerator
from test.test_signatues.mock_signature_generators.mock_atom_signature_generator import atom0, atom1, atom0_1


class MockLiteralSignatureGenerator(LiteralSignatureGenerator):
    def __init__(self):
        super().__init__(atom_gen=None)

    def generate(self):
        global literal0, literal1, literal1_neg, literal0_1
        yield literal0
        yield literal1
        yield literal1_neg
        yield literal0_1


literal0 = Literal(items=atom0, negated=False)
literal1 = Literal(items=atom1, negated=False)
literal1_neg = Literal(items=atom1, negated=True)
literal0_1 = Literal(items=atom0_1, negated=False)
