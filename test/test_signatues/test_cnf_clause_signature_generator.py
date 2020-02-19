from logic_formula_generator.generators._signatures.first_order_logic import CNFClauseGenerator

from logic_formula_generator.syntax_tree.first_order_logic import CNFClause
from test.test_signatues.mock_signature_generators.mock_literal_signature_generator import \
    MockLiteralGenerator, literal0, literal1, literal1_neg, literal0_1


class TestCNFClauseSignatureGenerator:
    def test_clause_length_empty(self):
        cg = CNFClauseGenerator(clause_lengths={}, literal_gen=MockLiteralGenerator())
        clauses = list(cg.generate)
        assert clauses == []

    def test_clause_length_0(self):
        cg = CNFClauseGenerator(clause_lengths={0}, literal_gen=MockLiteralGenerator())
        clauses = list(cg.generate)
        assert clauses == []

    def test_clause_length_1(self):
        cg = CNFClauseGenerator(clause_lengths={1}, literal_gen=MockLiteralGenerator())
        clauses = list(cg.generate)
        assert CNFClause(children=[literal0]).equivalent_in(clauses)
        assert CNFClause(children=[literal1]).equivalent_in(clauses)
        assert CNFClause(children=[literal1_neg]).equivalent_in(clauses)
        assert CNFClause(children=[literal0_1]).equivalent_in(clauses)
        assert len(clauses) == 4

    def test_clause_length_2(self):
        cg = CNFClauseGenerator(clause_lengths={2}, literal_gen=MockLiteralGenerator())
        clauses = list(cg.generate)
        assert CNFClause(children=[literal0, literal0]).equivalent_in(clauses)
        assert CNFClause(children=[literal0, literal1]).equivalent_in(clauses)
        assert CNFClause(children=[literal0, literal1_neg]).equivalent_in(clauses)
        assert CNFClause(children=[literal0, literal0_1]).equivalent_in(clauses)
        assert CNFClause(children=[literal1, literal1]).equivalent_in(clauses)
        assert CNFClause(children=[literal1, literal1_neg]).equivalent_in(clauses)
        assert CNFClause(children=[literal1, literal0_1]).equivalent_in(clauses)
        assert CNFClause(children=[literal1_neg, literal1_neg]).equivalent_in(clauses)
        assert CNFClause(children=[literal1_neg, literal0_1]).equivalent_in(clauses)
        assert CNFClause(children=[literal0_1, literal0_1]).equivalent_in(clauses)
        assert len(clauses) == 10
