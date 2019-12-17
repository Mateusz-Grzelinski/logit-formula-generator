from src.ast.first_order_logic import CNFFormula
from src.generators._signatures.first_order_logic import CNFFormulaGenerator
from test.test_signatues.mock_signature_generators.mock_cnf_clause_signature_generator import \
    MockCNFClauseGenerator, clause2_1, clause2, clause1_1, clause1


class TestCNFFormulaSignatureGenerator:
    def test_cnf_formula_clause_len_1(self):
        fg = CNFFormulaGenerator(clause_gens={MockCNFClauseGenerator(): 1})
        formulas = list(fg.generate())
        assert CNFFormula(items=[clause1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause1_1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause2]).equivalent_in(formulas)
        assert CNFFormula(items=[clause2_1]).equivalent_in(formulas)
        assert len(formulas) == 4

    def test_cnf_formula_clause_len_2(self):
        fg = CNFFormulaGenerator(clause_gens={MockCNFClauseGenerator(): 2})
        formulas = list(fg.generate())
        assert CNFFormula(items=[clause1, clause1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause1, clause1_1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause1, clause2]).equivalent_in(formulas)
        assert CNFFormula(items=[clause1, clause2_1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause1_1, clause1_1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause1_1, clause2]).equivalent_in(formulas)
        assert CNFFormula(items=[clause1_1, clause2_1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause2, clause2]).equivalent_in(formulas)
        assert CNFFormula(items=[clause2, clause2_1]).equivalent_in(formulas)
        assert CNFFormula(items=[clause2_1, clause2_1]).equivalent_in(formulas)
        assert len(formulas) == 10
