from __future__ import annotations

from src.ast import LogicalConnective
from src.ast.propositional_temporal_logic import TemporalLogicConnective
from src.ast.propositional_temporal_logic.info.cnf_ptl_formula_info import \
    ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo
from src.ast.propositional_temporal_logic.visitors.propositional_temporal_logic_visitor import \
    PropositionalTemporalLogicVisitor
from .._ptl_formula import PTLFormula
from .._variable import Variable


class CNFPTLFormulaVisitor(PropositionalTemporalLogicVisitor):
    def __init__(self):
        self.info = ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo()
        # no braces are generated so we can get away wothout context
        # self.context: Optional[PTLFormula] = None

    def visit_variable(self, element: Variable):
        self.info.number_of_variables += 1
        if not element.unary_connectives:
            self.info.number_of_variables_without_connective += 1
        elif any(TemporalLogicConnective.ALWAYS == e.connective for e in element.unary_connectives):
            self.info.number_of_variables_with_always_connectives += 1
        elif any(TemporalLogicConnective.EVENTUALLY == e.connective for e in element.unary_connectives):
            self.info.number_of_variables_with_eventually_connectives += 1
        # elif any(TemporalLogicConnective.ALWAYS == e.connective for e in element.unary_connectives):
        #     self.info.number_of_variables_with_both_connectives += 1

    def visit_temporal_logic_formula(self, element: PTLFormula):
        from src.ast import ConnectiveProperties
        element.logical_connective: ConnectiveProperties
        if LogicalConnective.OR == element.logical_connective.connective:
            # this is inside clause
            try:
                self.info.clause_sizes[len(element)] += 1
            except KeyError:
                self.info.clause_sizes[len(element)] = 1
        elif LogicalConnective.AND == element.logical_connective.connective:
            # this is root formula
            self.info.number_of_clauses = len(element)

        self.info.max_clause_size = max(list(self.info.clause_sizes.keys()) + [0])
