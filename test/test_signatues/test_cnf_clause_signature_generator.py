from src.ast.first_order_logic import CNFClause
from src.generators._signatures.first_order_logic import CNFClauseSignatureGenerator
from test.test_signatues.mock_signature_generators.mock_literal_signature_generator import \
    MockLiteralSignatureGenerator, literal0, literal1, literal1_neg, literal0_1


class TestCNFClauseSignatureGenerator:
    def test_clause_length_empty(self):
        cg = CNFClauseSignatureGenerator(clause_lengths={}, literal_gen=MockLiteralSignatureGenerator())
        clauses = list(cg.generate())
        assert clauses == []

    def test_clause_length_0(self):
        cg = CNFClauseSignatureGenerator(clause_lengths={0}, literal_gen=MockLiteralSignatureGenerator())
        clauses = list(cg.generate())
        assert clauses == []

    def test_clause_length_1(self):
        cg = CNFClauseSignatureGenerator(clause_lengths={1}, literal_gen=MockLiteralSignatureGenerator())
        clauses = list(cg.generate())
        assert CNFClause(items=[literal0]).equivalent_in(clauses)
        assert CNFClause(items=[literal1]).equivalent_in(clauses)
        assert CNFClause(items=[literal1_neg]).equivalent_in(clauses)
        assert CNFClause(items=[literal0_1]).equivalent_in(clauses)
        assert len(clauses) == 4

    def test_clause_length_2(self):
        cg = CNFClauseSignatureGenerator(clause_lengths={2}, literal_gen=MockLiteralSignatureGenerator())
        clauses = list(cg.generate())
        assert CNFClause(items=[literal0, literal0]).equivalent_in(clauses)
        assert CNFClause(items=[literal0, literal1]).equivalent_in(clauses)
        assert CNFClause(items=[literal0, literal1_neg]).equivalent_in(clauses)
        assert CNFClause(items=[literal0, literal0_1]).equivalent_in(clauses)
        assert CNFClause(items=[literal1, literal1]).equivalent_in(clauses)
        assert CNFClause(items=[literal1, literal1_neg]).equivalent_in(clauses)
        assert CNFClause(items=[literal1, literal0_1]).equivalent_in(clauses)
        assert CNFClause(items=[literal1_neg, literal1_neg]).equivalent_in(clauses)
        assert CNFClause(items=[literal1_neg, literal0_1]).equivalent_in(clauses)
        assert CNFClause(items=[literal0_1, literal0_1]).equivalent_in(clauses)
        assert len(clauses) == 10
