from typing import Generator

from src.generators._signatures.first_order_logic import CNFClauseGenerator

from src.syntax_tree.first_order_logic import CNFClause
from test.test_signatues.mock_signature_generators.mock_literal_signature_generator import literal0, literal1


class MockCNFClauseGenerator(CNFClauseGenerator):
    def __init__(self):
        super().__init__(clause_lengths={1, 2}, literal_gen=None)

    def generate(self) -> Generator[CNFClause, None, None]:
        global clause1, clause1_1, clause2, clause2_1
        yield clause1
        yield clause1_1
        yield clause2
        yield clause2_1


clause1 = CNFClause(children=[literal0])
clause1_1 = CNFClause(children=[literal1])

clause2 = CNFClause(children=[literal0, literal0])
clause2_1 = CNFClause(children=[literal0, literal1])
