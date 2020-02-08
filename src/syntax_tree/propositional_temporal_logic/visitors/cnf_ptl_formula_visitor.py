from __future__ import annotations

from src.syntax_tree import LogicalConnective
from src.syntax_tree.propositional_temporal_logic.info.cnf_ptl_formula_info import \
    ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo
from src.syntax_tree.propositional_temporal_logic.visitors.propositional_temporal_logic_visitor import \
    PropositionalTemporalLogicVisitor
from .._ptl_formula import PTLFormula
from .._variable import Variable
from ...connectives import TemporalLogicConnective


class CNFPTLFormulaVisitor(PropositionalTemporalLogicVisitor):
    def __init__(self):
        super().__init__()
        self.info = ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo()

    def visit_variable(self, element: Variable):
        self.info.number_of_variables += 1
        try:
            self.info.repeated_variables[element.name] += 1
        except KeyError:
            self.info.repeated_variables[element.name] = 1
        unary_connectives = element.unary_connectives
        if TemporalLogicConnective.ALWAYS in unary_connectives:
            self.info.number_of_variables_with_always_connectives += 1
        if TemporalLogicConnective.EVENTUALLY in unary_connectives:
            self.info.number_of_variables_with_eventually_connectives += 1
        if TemporalLogicConnective.ALWAYS not in unary_connectives \
                and TemporalLogicConnective.EVENTUALLY not in unary_connectives:
            self.info.number_of_variables_without_connective += 1
        if LogicalConnective.NOT in unary_connectives:
            self.info.number_of_negated_variables += 1
        # elif any(TemporalLogicConnective.ALWAYS == e.connective for e in element.unary_connectives):
        #     self.info.number_of_variables_with_both_connectives += 1

    def visit_temporal_logic_formula_pre(self, element: PTLFormula):
        if LogicalConnective.OR == element.logical_connective:
            # this is inside clause
            try:
                self.info.clause_sizes[len(element)] += 1
            except KeyError:
                self.info.clause_sizes[len(element)] = 1
        elif LogicalConnective.AND == element.logical_connective:
            # this is root formula
            self.info.number_of_clauses = len(element)

        self.info.max_clause_size = max(list(self.info.clause_sizes.keys()) + [0])
