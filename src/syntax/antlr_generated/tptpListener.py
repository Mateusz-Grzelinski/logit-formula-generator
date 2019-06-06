# Generated from tptp.g4 by ANTLR 4.7.2
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .tptpParser import tptpParser
else:
    from tptpParser import tptpParser


# This class defines a complete listener for a parse tree produced by tptpParser.
class tptpListener(ParseTreeListener):

    # Enter a parse tree produced by tptpParser#tptp_file.
    def enterTptp_file(self, ctx: tptpParser.Tptp_fileContext):
        pass

    # Exit a parse tree produced by tptpParser#tptp_file.
    def exitTptp_file(self, ctx: tptpParser.Tptp_fileContext):
        pass

    # Enter a parse tree produced by tptpParser#tptp_input.
    def enterTptp_input(self, ctx: tptpParser.Tptp_inputContext):
        pass

    # Exit a parse tree produced by tptpParser#tptp_input.
    def exitTptp_input(self, ctx: tptpParser.Tptp_inputContext):
        pass

    # Enter a parse tree produced by tptpParser#annotated_formula.
    def enterAnnotated_formula(self, ctx: tptpParser.Annotated_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#annotated_formula.
    def exitAnnotated_formula(self, ctx: tptpParser.Annotated_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tpi_annotated.
    def enterTpi_annotated(self, ctx: tptpParser.Tpi_annotatedContext):
        pass

    # Exit a parse tree produced by tptpParser#tpi_annotated.
    def exitTpi_annotated(self, ctx: tptpParser.Tpi_annotatedContext):
        pass

    # Enter a parse tree produced by tptpParser#tpi_formula.
    def enterTpi_formula(self, ctx: tptpParser.Tpi_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tpi_formula.
    def exitTpi_formula(self, ctx: tptpParser.Tpi_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_annotated.
    def enterThf_annotated(self, ctx: tptpParser.Thf_annotatedContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_annotated.
    def exitThf_annotated(self, ctx: tptpParser.Thf_annotatedContext):
        pass

    # Enter a parse tree produced by tptpParser#tfx_annotated.
    def enterTfx_annotated(self, ctx: tptpParser.Tfx_annotatedContext):
        pass

    # Exit a parse tree produced by tptpParser#tfx_annotated.
    def exitTfx_annotated(self, ctx: tptpParser.Tfx_annotatedContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_annotated.
    def enterTff_annotated(self, ctx: tptpParser.Tff_annotatedContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_annotated.
    def exitTff_annotated(self, ctx: tptpParser.Tff_annotatedContext):
        pass

    # Enter a parse tree produced by tptpParser#tcf_annotated.
    def enterTcf_annotated(self, ctx: tptpParser.Tcf_annotatedContext):
        pass

    # Exit a parse tree produced by tptpParser#tcf_annotated.
    def exitTcf_annotated(self, ctx: tptpParser.Tcf_annotatedContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_annotated.
    def enterFof_annotated(self, ctx: tptpParser.Fof_annotatedContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_annotated.
    def exitFof_annotated(self, ctx: tptpParser.Fof_annotatedContext):
        pass

    # Enter a parse tree produced by tptpParser#cnf_annotated.
    def enterCnf_annotated(self, ctx: tptpParser.Cnf_annotatedContext):
        pass

    # Exit a parse tree produced by tptpParser#cnf_annotated.
    def exitCnf_annotated(self, ctx: tptpParser.Cnf_annotatedContext):
        pass

    # Enter a parse tree produced by tptpParser#annotations.
    def enterAnnotations(self, ctx: tptpParser.AnnotationsContext):
        pass

    # Exit a parse tree produced by tptpParser#annotations.
    def exitAnnotations(self, ctx: tptpParser.AnnotationsContext):
        pass

    # Enter a parse tree produced by tptpParser#formula_role.
    def enterFormula_role(self, ctx: tptpParser.Formula_roleContext):
        pass

    # Exit a parse tree produced by tptpParser#formula_role.
    def exitFormula_role(self, ctx: tptpParser.Formula_roleContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_formula.
    def enterThf_formula(self, ctx: tptpParser.Thf_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_formula.
    def exitThf_formula(self, ctx: tptpParser.Thf_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_logic_formula.
    def enterThf_logic_formula(self, ctx: tptpParser.Thf_logic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_logic_formula.
    def exitThf_logic_formula(self, ctx: tptpParser.Thf_logic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_binary_formula.
    def enterThf_binary_formula(self, ctx: tptpParser.Thf_binary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_binary_formula.
    def exitThf_binary_formula(self, ctx: tptpParser.Thf_binary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_binary_pair.
    def enterThf_binary_pair(self, ctx: tptpParser.Thf_binary_pairContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_binary_pair.
    def exitThf_binary_pair(self, ctx: tptpParser.Thf_binary_pairContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_binary_tuple.
    def enterThf_binary_tuple(self, ctx: tptpParser.Thf_binary_tupleContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_binary_tuple.
    def exitThf_binary_tuple(self, ctx: tptpParser.Thf_binary_tupleContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_or_formula.
    def enterThf_or_formula(self, ctx: tptpParser.Thf_or_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_or_formula.
    def exitThf_or_formula(self, ctx: tptpParser.Thf_or_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_and_formula.
    def enterThf_and_formula(self, ctx: tptpParser.Thf_and_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_and_formula.
    def exitThf_and_formula(self, ctx: tptpParser.Thf_and_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_apply_formula.
    def enterThf_apply_formula(self, ctx: tptpParser.Thf_apply_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_apply_formula.
    def exitThf_apply_formula(self, ctx: tptpParser.Thf_apply_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_unitary_formula.
    def enterThf_unitary_formula(self, ctx: tptpParser.Thf_unitary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_unitary_formula.
    def exitThf_unitary_formula(self, ctx: tptpParser.Thf_unitary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_quantified_formula.
    def enterThf_quantified_formula(self, ctx: tptpParser.Thf_quantified_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_quantified_formula.
    def exitThf_quantified_formula(self, ctx: tptpParser.Thf_quantified_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_quantification.
    def enterThf_quantification(self, ctx: tptpParser.Thf_quantificationContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_quantification.
    def exitThf_quantification(self, ctx: tptpParser.Thf_quantificationContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_variable_list.
    def enterThf_variable_list(self, ctx: tptpParser.Thf_variable_listContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_variable_list.
    def exitThf_variable_list(self, ctx: tptpParser.Thf_variable_listContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_variable.
    def enterThf_variable(self, ctx: tptpParser.Thf_variableContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_variable.
    def exitThf_variable(self, ctx: tptpParser.Thf_variableContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_typed_variable.
    def enterThf_typed_variable(self, ctx: tptpParser.Thf_typed_variableContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_typed_variable.
    def exitThf_typed_variable(self, ctx: tptpParser.Thf_typed_variableContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_unary_formula.
    def enterThf_unary_formula(self, ctx: tptpParser.Thf_unary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_unary_formula.
    def exitThf_unary_formula(self, ctx: tptpParser.Thf_unary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_atom.
    def enterThf_atom(self, ctx: tptpParser.Thf_atomContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_atom.
    def exitThf_atom(self, ctx: tptpParser.Thf_atomContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_function.
    def enterThf_function(self, ctx: tptpParser.Thf_functionContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_function.
    def exitThf_function(self, ctx: tptpParser.Thf_functionContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_conn_term.
    def enterThf_conn_term(self, ctx: tptpParser.Thf_conn_termContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_conn_term.
    def exitThf_conn_term(self, ctx: tptpParser.Thf_conn_termContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_conditional.
    def enterThf_conditional(self, ctx: tptpParser.Thf_conditionalContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_conditional.
    def exitThf_conditional(self, ctx: tptpParser.Thf_conditionalContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_let.
    def enterThf_let(self, ctx: tptpParser.Thf_letContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_let.
    def exitThf_let(self, ctx: tptpParser.Thf_letContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_arguments.
    def enterThf_arguments(self, ctx: tptpParser.Thf_argumentsContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_arguments.
    def exitThf_arguments(self, ctx: tptpParser.Thf_argumentsContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_type_formula.
    def enterThf_type_formula(self, ctx: tptpParser.Thf_type_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_type_formula.
    def exitThf_type_formula(self, ctx: tptpParser.Thf_type_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_typeable_formula.
    def enterThf_typeable_formula(self, ctx: tptpParser.Thf_typeable_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_typeable_formula.
    def exitThf_typeable_formula(self, ctx: tptpParser.Thf_typeable_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_subtype.
    def enterThf_subtype(self, ctx: tptpParser.Thf_subtypeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_subtype.
    def exitThf_subtype(self, ctx: tptpParser.Thf_subtypeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_top_level_type.
    def enterThf_top_level_type(self, ctx: tptpParser.Thf_top_level_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_top_level_type.
    def exitThf_top_level_type(self, ctx: tptpParser.Thf_top_level_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_unitary_type.
    def enterThf_unitary_type(self, ctx: tptpParser.Thf_unitary_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_unitary_type.
    def exitThf_unitary_type(self, ctx: tptpParser.Thf_unitary_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_apply_type.
    def enterThf_apply_type(self, ctx: tptpParser.Thf_apply_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_apply_type.
    def exitThf_apply_type(self, ctx: tptpParser.Thf_apply_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_binary_type.
    def enterThf_binary_type(self, ctx: tptpParser.Thf_binary_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_binary_type.
    def exitThf_binary_type(self, ctx: tptpParser.Thf_binary_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_mapping_type.
    def enterThf_mapping_type(self, ctx: tptpParser.Thf_mapping_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_mapping_type.
    def exitThf_mapping_type(self, ctx: tptpParser.Thf_mapping_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_xprod_type.
    def enterThf_xprod_type(self, ctx: tptpParser.Thf_xprod_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_xprod_type.
    def exitThf_xprod_type(self, ctx: tptpParser.Thf_xprod_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_union_type.
    def enterThf_union_type(self, ctx: tptpParser.Thf_union_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_union_type.
    def exitThf_union_type(self, ctx: tptpParser.Thf_union_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_sequent.
    def enterThf_sequent(self, ctx: tptpParser.Thf_sequentContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_sequent.
    def exitThf_sequent(self, ctx: tptpParser.Thf_sequentContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_tuple.
    def enterThf_tuple(self, ctx: tptpParser.Thf_tupleContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_tuple.
    def exitThf_tuple(self, ctx: tptpParser.Thf_tupleContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_formula_list.
    def enterThf_formula_list(self, ctx: tptpParser.Thf_formula_listContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_formula_list.
    def exitThf_formula_list(self, ctx: tptpParser.Thf_formula_listContext):
        pass

    # Enter a parse tree produced by tptpParser#tfx_formula.
    def enterTfx_formula(self, ctx: tptpParser.Tfx_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tfx_formula.
    def exitTfx_formula(self, ctx: tptpParser.Tfx_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tfx_logic_formula.
    def enterTfx_logic_formula(self, ctx: tptpParser.Tfx_logic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tfx_logic_formula.
    def exitTfx_logic_formula(self, ctx: tptpParser.Tfx_logic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_formula.
    def enterTff_formula(self, ctx: tptpParser.Tff_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_formula.
    def exitTff_formula(self, ctx: tptpParser.Tff_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_logic_formula.
    def enterTff_logic_formula(self, ctx: tptpParser.Tff_logic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_logic_formula.
    def exitTff_logic_formula(self, ctx: tptpParser.Tff_logic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_binary_formula.
    def enterTff_binary_formula(self, ctx: tptpParser.Tff_binary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_binary_formula.
    def exitTff_binary_formula(self, ctx: tptpParser.Tff_binary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_binary_nonassoc.
    def enterTff_binary_nonassoc(self, ctx: tptpParser.Tff_binary_nonassocContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_binary_nonassoc.
    def exitTff_binary_nonassoc(self, ctx: tptpParser.Tff_binary_nonassocContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_binary_assoc.
    def enterTff_binary_assoc(self, ctx: tptpParser.Tff_binary_assocContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_binary_assoc.
    def exitTff_binary_assoc(self, ctx: tptpParser.Tff_binary_assocContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_or_formula.
    def enterTff_or_formula(self, ctx: tptpParser.Tff_or_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_or_formula.
    def exitTff_or_formula(self, ctx: tptpParser.Tff_or_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_and_formula.
    def enterTff_and_formula(self, ctx: tptpParser.Tff_and_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_and_formula.
    def exitTff_and_formula(self, ctx: tptpParser.Tff_and_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_unitary_formula.
    def enterTff_unitary_formula(self, ctx: tptpParser.Tff_unitary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_unitary_formula.
    def exitTff_unitary_formula(self, ctx: tptpParser.Tff_unitary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_quantified_formula.
    def enterTff_quantified_formula(self, ctx: tptpParser.Tff_quantified_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_quantified_formula.
    def exitTff_quantified_formula(self, ctx: tptpParser.Tff_quantified_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_variable_list.
    def enterTff_variable_list(self, ctx: tptpParser.Tff_variable_listContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_variable_list.
    def exitTff_variable_list(self, ctx: tptpParser.Tff_variable_listContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_variable.
    def enterTff_variable(self, ctx: tptpParser.Tff_variableContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_variable.
    def exitTff_variable(self, ctx: tptpParser.Tff_variableContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_typed_variable.
    def enterTff_typed_variable(self, ctx: tptpParser.Tff_typed_variableContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_typed_variable.
    def exitTff_typed_variable(self, ctx: tptpParser.Tff_typed_variableContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_unary_formula.
    def enterTff_unary_formula(self, ctx: tptpParser.Tff_unary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_unary_formula.
    def exitTff_unary_formula(self, ctx: tptpParser.Tff_unary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_atomic_formula.
    def enterTff_atomic_formula(self, ctx: tptpParser.Tff_atomic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_atomic_formula.
    def exitTff_atomic_formula(self, ctx: tptpParser.Tff_atomic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_conditional.
    def enterTff_conditional(self, ctx: tptpParser.Tff_conditionalContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_conditional.
    def exitTff_conditional(self, ctx: tptpParser.Tff_conditionalContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let.
    def enterTff_let(self, ctx: tptpParser.Tff_letContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let.
    def exitTff_let(self, ctx: tptpParser.Tff_letContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_term_defns.
    def enterTff_let_term_defns(self, ctx: tptpParser.Tff_let_term_defnsContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_term_defns.
    def exitTff_let_term_defns(self, ctx: tptpParser.Tff_let_term_defnsContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_term_list.
    def enterTff_let_term_list(self, ctx: tptpParser.Tff_let_term_listContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_term_list.
    def exitTff_let_term_list(self, ctx: tptpParser.Tff_let_term_listContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_term_defn.
    def enterTff_let_term_defn(self, ctx: tptpParser.Tff_let_term_defnContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_term_defn.
    def exitTff_let_term_defn(self, ctx: tptpParser.Tff_let_term_defnContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_term_binding.
    def enterTff_let_term_binding(self, ctx: tptpParser.Tff_let_term_bindingContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_term_binding.
    def exitTff_let_term_binding(self, ctx: tptpParser.Tff_let_term_bindingContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_formula_defns.
    def enterTff_let_formula_defns(self, ctx: tptpParser.Tff_let_formula_defnsContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_formula_defns.
    def exitTff_let_formula_defns(self, ctx: tptpParser.Tff_let_formula_defnsContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_formula_list.
    def enterTff_let_formula_list(self, ctx: tptpParser.Tff_let_formula_listContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_formula_list.
    def exitTff_let_formula_list(self, ctx: tptpParser.Tff_let_formula_listContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_formula_defn.
    def enterTff_let_formula_defn(self, ctx: tptpParser.Tff_let_formula_defnContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_formula_defn.
    def exitTff_let_formula_defn(self, ctx: tptpParser.Tff_let_formula_defnContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_formula_binding.
    def enterTff_let_formula_binding(self, ctx: tptpParser.Tff_let_formula_bindingContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_formula_binding.
    def exitTff_let_formula_binding(self, ctx: tptpParser.Tff_let_formula_bindingContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_sequent.
    def enterTff_sequent(self, ctx: tptpParser.Tff_sequentContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_sequent.
    def exitTff_sequent(self, ctx: tptpParser.Tff_sequentContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_formula_tuple.
    def enterTff_formula_tuple(self, ctx: tptpParser.Tff_formula_tupleContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_formula_tuple.
    def exitTff_formula_tuple(self, ctx: tptpParser.Tff_formula_tupleContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_formula_tuple_list.
    def enterTff_formula_tuple_list(self, ctx: tptpParser.Tff_formula_tuple_listContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_formula_tuple_list.
    def exitTff_formula_tuple_list(self, ctx: tptpParser.Tff_formula_tuple_listContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_typed_atom.
    def enterTff_typed_atom(self, ctx: tptpParser.Tff_typed_atomContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_typed_atom.
    def exitTff_typed_atom(self, ctx: tptpParser.Tff_typed_atomContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_subtype.
    def enterTff_subtype(self, ctx: tptpParser.Tff_subtypeContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_subtype.
    def exitTff_subtype(self, ctx: tptpParser.Tff_subtypeContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_top_level_type.
    def enterTff_top_level_type(self, ctx: tptpParser.Tff_top_level_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_top_level_type.
    def exitTff_top_level_type(self, ctx: tptpParser.Tff_top_level_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#tf1_quantified_type.
    def enterTf1_quantified_type(self, ctx: tptpParser.Tf1_quantified_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#tf1_quantified_type.
    def exitTf1_quantified_type(self, ctx: tptpParser.Tf1_quantified_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_monotype.
    def enterTff_monotype(self, ctx: tptpParser.Tff_monotypeContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_monotype.
    def exitTff_monotype(self, ctx: tptpParser.Tff_monotypeContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_unitary_type.
    def enterTff_unitary_type(self, ctx: tptpParser.Tff_unitary_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_unitary_type.
    def exitTff_unitary_type(self, ctx: tptpParser.Tff_unitary_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_atomic_type.
    def enterTff_atomic_type(self, ctx: tptpParser.Tff_atomic_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_atomic_type.
    def exitTff_atomic_type(self, ctx: tptpParser.Tff_atomic_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_type_arguments.
    def enterTff_type_arguments(self, ctx: tptpParser.Tff_type_argumentsContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_type_arguments.
    def exitTff_type_arguments(self, ctx: tptpParser.Tff_type_argumentsContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_mapping_type.
    def enterTff_mapping_type(self, ctx: tptpParser.Tff_mapping_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_mapping_type.
    def exitTff_mapping_type(self, ctx: tptpParser.Tff_mapping_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_xprod_type.
    def enterTff_xprod_type(self, ctx: tptpParser.Tff_xprod_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_xprod_type.
    def exitTff_xprod_type(self, ctx: tptpParser.Tff_xprod_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#tcf_formula.
    def enterTcf_formula(self, ctx: tptpParser.Tcf_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tcf_formula.
    def exitTcf_formula(self, ctx: tptpParser.Tcf_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tcf_logic_formula.
    def enterTcf_logic_formula(self, ctx: tptpParser.Tcf_logic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tcf_logic_formula.
    def exitTcf_logic_formula(self, ctx: tptpParser.Tcf_logic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#tcf_quantified_formula.
    def enterTcf_quantified_formula(self, ctx: tptpParser.Tcf_quantified_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#tcf_quantified_formula.
    def exitTcf_quantified_formula(self, ctx: tptpParser.Tcf_quantified_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_formula.
    def enterFof_formula(self, ctx: tptpParser.Fof_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_formula.
    def exitFof_formula(self, ctx: tptpParser.Fof_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_logic_formula.
    def enterFof_logic_formula(self, ctx: tptpParser.Fof_logic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_logic_formula.
    def exitFof_logic_formula(self, ctx: tptpParser.Fof_logic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_binary_formula.
    def enterFof_binary_formula(self, ctx: tptpParser.Fof_binary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_binary_formula.
    def exitFof_binary_formula(self, ctx: tptpParser.Fof_binary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_binary_nonassoc.
    def enterFof_binary_nonassoc(self, ctx: tptpParser.Fof_binary_nonassocContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_binary_nonassoc.
    def exitFof_binary_nonassoc(self, ctx: tptpParser.Fof_binary_nonassocContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_binary_assoc.
    def enterFof_binary_assoc(self, ctx: tptpParser.Fof_binary_assocContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_binary_assoc.
    def exitFof_binary_assoc(self, ctx: tptpParser.Fof_binary_assocContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_or_formula.
    def enterFof_or_formula(self, ctx: tptpParser.Fof_or_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_or_formula.
    def exitFof_or_formula(self, ctx: tptpParser.Fof_or_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_and_formula.
    def enterFof_and_formula(self, ctx: tptpParser.Fof_and_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_and_formula.
    def exitFof_and_formula(self, ctx: tptpParser.Fof_and_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_unitary_formula.
    def enterFof_unitary_formula(self, ctx: tptpParser.Fof_unitary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_unitary_formula.
    def exitFof_unitary_formula(self, ctx: tptpParser.Fof_unitary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_quantified_formula.
    def enterFof_quantified_formula(self, ctx: tptpParser.Fof_quantified_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_quantified_formula.
    def exitFof_quantified_formula(self, ctx: tptpParser.Fof_quantified_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_variable_list.
    def enterFof_variable_list(self, ctx: tptpParser.Fof_variable_listContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_variable_list.
    def exitFof_variable_list(self, ctx: tptpParser.Fof_variable_listContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_unary_formula.
    def enterFof_unary_formula(self, ctx: tptpParser.Fof_unary_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_unary_formula.
    def exitFof_unary_formula(self, ctx: tptpParser.Fof_unary_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_infix_unary.
    def enterFof_infix_unary(self, ctx: tptpParser.Fof_infix_unaryContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_infix_unary.
    def exitFof_infix_unary(self, ctx: tptpParser.Fof_infix_unaryContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_atomic_formula.
    def enterFof_atomic_formula(self, ctx: tptpParser.Fof_atomic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_atomic_formula.
    def exitFof_atomic_formula(self, ctx: tptpParser.Fof_atomic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_plain_atomic_formula.
    def enterFof_plain_atomic_formula(self, ctx: tptpParser.Fof_plain_atomic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_plain_atomic_formula.
    def exitFof_plain_atomic_formula(self, ctx: tptpParser.Fof_plain_atomic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_defined_atomic_formula.
    def enterFof_defined_atomic_formula(self, ctx: tptpParser.Fof_defined_atomic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_defined_atomic_formula.
    def exitFof_defined_atomic_formula(self, ctx: tptpParser.Fof_defined_atomic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_defined_plain_formula.
    def enterFof_defined_plain_formula(self, ctx: tptpParser.Fof_defined_plain_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_defined_plain_formula.
    def exitFof_defined_plain_formula(self, ctx: tptpParser.Fof_defined_plain_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_defined_infix_formula.
    def enterFof_defined_infix_formula(self, ctx: tptpParser.Fof_defined_infix_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_defined_infix_formula.
    def exitFof_defined_infix_formula(self, ctx: tptpParser.Fof_defined_infix_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_system_atomic_formula.
    def enterFof_system_atomic_formula(self, ctx: tptpParser.Fof_system_atomic_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_system_atomic_formula.
    def exitFof_system_atomic_formula(self, ctx: tptpParser.Fof_system_atomic_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_plain_term.
    def enterFof_plain_term(self, ctx: tptpParser.Fof_plain_termContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_plain_term.
    def exitFof_plain_term(self, ctx: tptpParser.Fof_plain_termContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_defined_term.
    def enterFof_defined_term(self, ctx: tptpParser.Fof_defined_termContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_defined_term.
    def exitFof_defined_term(self, ctx: tptpParser.Fof_defined_termContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_defined_atomic_term.
    def enterFof_defined_atomic_term(self, ctx: tptpParser.Fof_defined_atomic_termContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_defined_atomic_term.
    def exitFof_defined_atomic_term(self, ctx: tptpParser.Fof_defined_atomic_termContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_defined_plain_term.
    def enterFof_defined_plain_term(self, ctx: tptpParser.Fof_defined_plain_termContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_defined_plain_term.
    def exitFof_defined_plain_term(self, ctx: tptpParser.Fof_defined_plain_termContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_system_term.
    def enterFof_system_term(self, ctx: tptpParser.Fof_system_termContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_system_term.
    def exitFof_system_term(self, ctx: tptpParser.Fof_system_termContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_arguments.
    def enterFof_arguments(self, ctx: tptpParser.Fof_argumentsContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_arguments.
    def exitFof_arguments(self, ctx: tptpParser.Fof_argumentsContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_term.
    def enterFof_term(self, ctx: tptpParser.Fof_termContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_term.
    def exitFof_term(self, ctx: tptpParser.Fof_termContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_function_term.
    def enterFof_function_term(self, ctx: tptpParser.Fof_function_termContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_function_term.
    def exitFof_function_term(self, ctx: tptpParser.Fof_function_termContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_conditional_term.
    def enterTff_conditional_term(self, ctx: tptpParser.Tff_conditional_termContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_conditional_term.
    def exitTff_conditional_term(self, ctx: tptpParser.Tff_conditional_termContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_let_term.
    def enterTff_let_term(self, ctx: tptpParser.Tff_let_termContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_let_term.
    def exitTff_let_term(self, ctx: tptpParser.Tff_let_termContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_tuple_term.
    def enterTff_tuple_term(self, ctx: tptpParser.Tff_tuple_termContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_tuple_term.
    def exitTff_tuple_term(self, ctx: tptpParser.Tff_tuple_termContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_sequent.
    def enterFof_sequent(self, ctx: tptpParser.Fof_sequentContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_sequent.
    def exitFof_sequent(self, ctx: tptpParser.Fof_sequentContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_formula_tuple.
    def enterFof_formula_tuple(self, ctx: tptpParser.Fof_formula_tupleContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_formula_tuple.
    def exitFof_formula_tuple(self, ctx: tptpParser.Fof_formula_tupleContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_formula_tuple_list.
    def enterFof_formula_tuple_list(self, ctx: tptpParser.Fof_formula_tuple_listContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_formula_tuple_list.
    def exitFof_formula_tuple_list(self, ctx: tptpParser.Fof_formula_tuple_listContext):
        pass

    # Enter a parse tree produced by tptpParser#cnf_formula.
    def enterCnf_formula(self, ctx: tptpParser.Cnf_formulaContext):
        pass

    # Exit a parse tree produced by tptpParser#cnf_formula.
    def exitCnf_formula(self, ctx: tptpParser.Cnf_formulaContext):
        pass

    # Enter a parse tree produced by tptpParser#cnf_disjunction.
    def enterCnf_disjunction(self, ctx: tptpParser.Cnf_disjunctionContext):
        pass

    # Exit a parse tree produced by tptpParser#cnf_disjunction.
    def exitCnf_disjunction(self, ctx: tptpParser.Cnf_disjunctionContext):
        pass

    # Enter a parse tree produced by tptpParser#cnf_literal.
    def enterCnf_literal(self, ctx: tptpParser.Cnf_literalContext):
        pass

    # Exit a parse tree produced by tptpParser#cnf_literal.
    def exitCnf_literal(self, ctx: tptpParser.Cnf_literalContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_quantifier.
    def enterThf_quantifier(self, ctx: tptpParser.Thf_quantifierContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_quantifier.
    def exitThf_quantifier(self, ctx: tptpParser.Thf_quantifierContext):
        pass

    # Enter a parse tree produced by tptpParser#th0_quantifier.
    def enterTh0_quantifier(self, ctx: tptpParser.Th0_quantifierContext):
        pass

    # Exit a parse tree produced by tptpParser#th0_quantifier.
    def exitTh0_quantifier(self, ctx: tptpParser.Th0_quantifierContext):
        pass

    # Enter a parse tree produced by tptpParser#th1_quantifier.
    def enterTh1_quantifier(self, ctx: tptpParser.Th1_quantifierContext):
        pass

    # Exit a parse tree produced by tptpParser#th1_quantifier.
    def exitTh1_quantifier(self, ctx: tptpParser.Th1_quantifierContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_pair_connective.
    def enterThf_pair_connective(self, ctx: tptpParser.Thf_pair_connectiveContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_pair_connective.
    def exitThf_pair_connective(self, ctx: tptpParser.Thf_pair_connectiveContext):
        pass

    # Enter a parse tree produced by tptpParser#thf_unary_connective.
    def enterThf_unary_connective(self, ctx: tptpParser.Thf_unary_connectiveContext):
        pass

    # Exit a parse tree produced by tptpParser#thf_unary_connective.
    def exitThf_unary_connective(self, ctx: tptpParser.Thf_unary_connectiveContext):
        pass

    # Enter a parse tree produced by tptpParser#th1_unary_connective.
    def enterTh1_unary_connective(self, ctx: tptpParser.Th1_unary_connectiveContext):
        pass

    # Exit a parse tree produced by tptpParser#th1_unary_connective.
    def exitTh1_unary_connective(self, ctx: tptpParser.Th1_unary_connectiveContext):
        pass

    # Enter a parse tree produced by tptpParser#tff_pair_connective.
    def enterTff_pair_connective(self, ctx: tptpParser.Tff_pair_connectiveContext):
        pass

    # Exit a parse tree produced by tptpParser#tff_pair_connective.
    def exitTff_pair_connective(self, ctx: tptpParser.Tff_pair_connectiveContext):
        pass

    # Enter a parse tree produced by tptpParser#fof_quantifier.
    def enterFof_quantifier(self, ctx: tptpParser.Fof_quantifierContext):
        pass

    # Exit a parse tree produced by tptpParser#fof_quantifier.
    def exitFof_quantifier(self, ctx: tptpParser.Fof_quantifierContext):
        pass

    # Enter a parse tree produced by tptpParser#binary_connective.
    def enterBinary_connective(self, ctx: tptpParser.Binary_connectiveContext):
        pass

    # Exit a parse tree produced by tptpParser#binary_connective.
    def exitBinary_connective(self, ctx: tptpParser.Binary_connectiveContext):
        pass

    # Enter a parse tree produced by tptpParser#assoc_connective.
    def enterAssoc_connective(self, ctx: tptpParser.Assoc_connectiveContext):
        pass

    # Exit a parse tree produced by tptpParser#assoc_connective.
    def exitAssoc_connective(self, ctx: tptpParser.Assoc_connectiveContext):
        pass

    # Enter a parse tree produced by tptpParser#unary_connective.
    def enterUnary_connective(self, ctx: tptpParser.Unary_connectiveContext):
        pass

    # Exit a parse tree produced by tptpParser#unary_connective.
    def exitUnary_connective(self, ctx: tptpParser.Unary_connectiveContext):
        pass

    # Enter a parse tree produced by tptpParser#type_constant.
    def enterType_constant(self, ctx: tptpParser.Type_constantContext):
        pass

    # Exit a parse tree produced by tptpParser#type_constant.
    def exitType_constant(self, ctx: tptpParser.Type_constantContext):
        pass

    # Enter a parse tree produced by tptpParser#type_functor.
    def enterType_functor(self, ctx: tptpParser.Type_functorContext):
        pass

    # Exit a parse tree produced by tptpParser#type_functor.
    def exitType_functor(self, ctx: tptpParser.Type_functorContext):
        pass

    # Enter a parse tree produced by tptpParser#defined_type.
    def enterDefined_type(self, ctx: tptpParser.Defined_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#defined_type.
    def exitDefined_type(self, ctx: tptpParser.Defined_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#system_type.
    def enterSystem_type(self, ctx: tptpParser.System_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#system_type.
    def exitSystem_type(self, ctx: tptpParser.System_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#atom.
    def enterAtom(self, ctx: tptpParser.AtomContext):
        pass

    # Exit a parse tree produced by tptpParser#atom.
    def exitAtom(self, ctx: tptpParser.AtomContext):
        pass

    # Enter a parse tree produced by tptpParser#untyped_atom.
    def enterUntyped_atom(self, ctx: tptpParser.Untyped_atomContext):
        pass

    # Exit a parse tree produced by tptpParser#untyped_atom.
    def exitUntyped_atom(self, ctx: tptpParser.Untyped_atomContext):
        pass

    # Enter a parse tree produced by tptpParser#defined_proposition.
    def enterDefined_proposition(self, ctx: tptpParser.Defined_propositionContext):
        pass

    # Exit a parse tree produced by tptpParser#defined_proposition.
    def exitDefined_proposition(self, ctx: tptpParser.Defined_propositionContext):
        pass

    # Enter a parse tree produced by tptpParser#defined_predicate.
    def enterDefined_predicate(self, ctx: tptpParser.Defined_predicateContext):
        pass

    # Exit a parse tree produced by tptpParser#defined_predicate.
    def exitDefined_predicate(self, ctx: tptpParser.Defined_predicateContext):
        pass

    # Enter a parse tree produced by tptpParser#defined_infix_pred.
    def enterDefined_infix_pred(self, ctx: tptpParser.Defined_infix_predContext):
        pass

    # Exit a parse tree produced by tptpParser#defined_infix_pred.
    def exitDefined_infix_pred(self, ctx: tptpParser.Defined_infix_predContext):
        pass

    # Enter a parse tree produced by tptpParser#constant.
    def enterConstant(self, ctx: tptpParser.ConstantContext):
        pass

    # Exit a parse tree produced by tptpParser#constant.
    def exitConstant(self, ctx: tptpParser.ConstantContext):
        pass

    # Enter a parse tree produced by tptpParser#functor.
    def enterFunctor(self, ctx: tptpParser.FunctorContext):
        pass

    # Exit a parse tree produced by tptpParser#functor.
    def exitFunctor(self, ctx: tptpParser.FunctorContext):
        pass

    # Enter a parse tree produced by tptpParser#system_constant.
    def enterSystem_constant(self, ctx: tptpParser.System_constantContext):
        pass

    # Exit a parse tree produced by tptpParser#system_constant.
    def exitSystem_constant(self, ctx: tptpParser.System_constantContext):
        pass

    # Enter a parse tree produced by tptpParser#system_functor.
    def enterSystem_functor(self, ctx: tptpParser.System_functorContext):
        pass

    # Exit a parse tree produced by tptpParser#system_functor.
    def exitSystem_functor(self, ctx: tptpParser.System_functorContext):
        pass

    # Enter a parse tree produced by tptpParser#defined_constant.
    def enterDefined_constant(self, ctx: tptpParser.Defined_constantContext):
        pass

    # Exit a parse tree produced by tptpParser#defined_constant.
    def exitDefined_constant(self, ctx: tptpParser.Defined_constantContext):
        pass

    # Enter a parse tree produced by tptpParser#defined_functor.
    def enterDefined_functor(self, ctx: tptpParser.Defined_functorContext):
        pass

    # Exit a parse tree produced by tptpParser#defined_functor.
    def exitDefined_functor(self, ctx: tptpParser.Defined_functorContext):
        pass

    # Enter a parse tree produced by tptpParser#defined_term.
    def enterDefined_term(self, ctx: tptpParser.Defined_termContext):
        pass

    # Exit a parse tree produced by tptpParser#defined_term.
    def exitDefined_term(self, ctx: tptpParser.Defined_termContext):
        pass

    # Enter a parse tree produced by tptpParser#variable.
    def enterVariable(self, ctx: tptpParser.VariableContext):
        pass

    # Exit a parse tree produced by tptpParser#variable.
    def exitVariable(self, ctx: tptpParser.VariableContext):
        pass

    # Enter a parse tree produced by tptpParser#source.
    def enterSource(self, ctx: tptpParser.SourceContext):
        pass

    # Exit a parse tree produced by tptpParser#source.
    def exitSource(self, ctx: tptpParser.SourceContext):
        pass

    # Enter a parse tree produced by tptpParser#sources.
    def enterSources(self, ctx: tptpParser.SourcesContext):
        pass

    # Exit a parse tree produced by tptpParser#sources.
    def exitSources(self, ctx: tptpParser.SourcesContext):
        pass

    # Enter a parse tree produced by tptpParser#dag_source.
    def enterDag_source(self, ctx: tptpParser.Dag_sourceContext):
        pass

    # Exit a parse tree produced by tptpParser#dag_source.
    def exitDag_source(self, ctx: tptpParser.Dag_sourceContext):
        pass

    # Enter a parse tree produced by tptpParser#inference_record.
    def enterInference_record(self, ctx: tptpParser.Inference_recordContext):
        pass

    # Exit a parse tree produced by tptpParser#inference_record.
    def exitInference_record(self, ctx: tptpParser.Inference_recordContext):
        pass

    # Enter a parse tree produced by tptpParser#inference_rule.
    def enterInference_rule(self, ctx: tptpParser.Inference_ruleContext):
        pass

    # Exit a parse tree produced by tptpParser#inference_rule.
    def exitInference_rule(self, ctx: tptpParser.Inference_ruleContext):
        pass

    # Enter a parse tree produced by tptpParser#inference_parents.
    def enterInference_parents(self, ctx: tptpParser.Inference_parentsContext):
        pass

    # Exit a parse tree produced by tptpParser#inference_parents.
    def exitInference_parents(self, ctx: tptpParser.Inference_parentsContext):
        pass

    # Enter a parse tree produced by tptpParser#parent_list.
    def enterParent_list(self, ctx: tptpParser.Parent_listContext):
        pass

    # Exit a parse tree produced by tptpParser#parent_list.
    def exitParent_list(self, ctx: tptpParser.Parent_listContext):
        pass

    # Enter a parse tree produced by tptpParser#parent_info.
    def enterParent_info(self, ctx: tptpParser.Parent_infoContext):
        pass

    # Exit a parse tree produced by tptpParser#parent_info.
    def exitParent_info(self, ctx: tptpParser.Parent_infoContext):
        pass

    # Enter a parse tree produced by tptpParser#parent_details.
    def enterParent_details(self, ctx: tptpParser.Parent_detailsContext):
        pass

    # Exit a parse tree produced by tptpParser#parent_details.
    def exitParent_details(self, ctx: tptpParser.Parent_detailsContext):
        pass

    # Enter a parse tree produced by tptpParser#internal_source.
    def enterInternal_source(self, ctx: tptpParser.Internal_sourceContext):
        pass

    # Exit a parse tree produced by tptpParser#internal_source.
    def exitInternal_source(self, ctx: tptpParser.Internal_sourceContext):
        pass

    # Enter a parse tree produced by tptpParser#intro_type.
    def enterIntro_type(self, ctx: tptpParser.Intro_typeContext):
        pass

    # Exit a parse tree produced by tptpParser#intro_type.
    def exitIntro_type(self, ctx: tptpParser.Intro_typeContext):
        pass

    # Enter a parse tree produced by tptpParser#external_source.
    def enterExternal_source(self, ctx: tptpParser.External_sourceContext):
        pass

    # Exit a parse tree produced by tptpParser#external_source.
    def exitExternal_source(self, ctx: tptpParser.External_sourceContext):
        pass

    # Enter a parse tree produced by tptpParser#file_source.
    def enterFile_source(self, ctx: tptpParser.File_sourceContext):
        pass

    # Exit a parse tree produced by tptpParser#file_source.
    def exitFile_source(self, ctx: tptpParser.File_sourceContext):
        pass

    # Enter a parse tree produced by tptpParser#file_info.
    def enterFile_info(self, ctx: tptpParser.File_infoContext):
        pass

    # Exit a parse tree produced by tptpParser#file_info.
    def exitFile_info(self, ctx: tptpParser.File_infoContext):
        pass

    # Enter a parse tree produced by tptpParser#theory.
    def enterTheory(self, ctx: tptpParser.TheoryContext):
        pass

    # Exit a parse tree produced by tptpParser#theory.
    def exitTheory(self, ctx: tptpParser.TheoryContext):
        pass

    # Enter a parse tree produced by tptpParser#theory_name.
    def enterTheory_name(self, ctx: tptpParser.Theory_nameContext):
        pass

    # Exit a parse tree produced by tptpParser#theory_name.
    def exitTheory_name(self, ctx: tptpParser.Theory_nameContext):
        pass

    # Enter a parse tree produced by tptpParser#creator_source.
    def enterCreator_source(self, ctx: tptpParser.Creator_sourceContext):
        pass

    # Exit a parse tree produced by tptpParser#creator_source.
    def exitCreator_source(self, ctx: tptpParser.Creator_sourceContext):
        pass

    # Enter a parse tree produced by tptpParser#creator_name.
    def enterCreator_name(self, ctx: tptpParser.Creator_nameContext):
        pass

    # Exit a parse tree produced by tptpParser#creator_name.
    def exitCreator_name(self, ctx: tptpParser.Creator_nameContext):
        pass

    # Enter a parse tree produced by tptpParser#optional_info.
    def enterOptional_info(self, ctx: tptpParser.Optional_infoContext):
        pass

    # Exit a parse tree produced by tptpParser#optional_info.
    def exitOptional_info(self, ctx: tptpParser.Optional_infoContext):
        pass

    # Enter a parse tree produced by tptpParser#useful_info.
    def enterUseful_info(self, ctx: tptpParser.Useful_infoContext):
        pass

    # Exit a parse tree produced by tptpParser#useful_info.
    def exitUseful_info(self, ctx: tptpParser.Useful_infoContext):
        pass

    # Enter a parse tree produced by tptpParser#info_items.
    def enterInfo_items(self, ctx: tptpParser.Info_itemsContext):
        pass

    # Exit a parse tree produced by tptpParser#info_items.
    def exitInfo_items(self, ctx: tptpParser.Info_itemsContext):
        pass

    # Enter a parse tree produced by tptpParser#info_item.
    def enterInfo_item(self, ctx: tptpParser.Info_itemContext):
        pass

    # Exit a parse tree produced by tptpParser#info_item.
    def exitInfo_item(self, ctx: tptpParser.Info_itemContext):
        pass

    # Enter a parse tree produced by tptpParser#formula_item.
    def enterFormula_item(self, ctx: tptpParser.Formula_itemContext):
        pass

    # Exit a parse tree produced by tptpParser#formula_item.
    def exitFormula_item(self, ctx: tptpParser.Formula_itemContext):
        pass

    # Enter a parse tree produced by tptpParser#description_item.
    def enterDescription_item(self, ctx: tptpParser.Description_itemContext):
        pass

    # Exit a parse tree produced by tptpParser#description_item.
    def exitDescription_item(self, ctx: tptpParser.Description_itemContext):
        pass

    # Enter a parse tree produced by tptpParser#iquote_item.
    def enterIquote_item(self, ctx: tptpParser.Iquote_itemContext):
        pass

    # Exit a parse tree produced by tptpParser#iquote_item.
    def exitIquote_item(self, ctx: tptpParser.Iquote_itemContext):
        pass

    # Enter a parse tree produced by tptpParser#inference_item.
    def enterInference_item(self, ctx: tptpParser.Inference_itemContext):
        pass

    # Exit a parse tree produced by tptpParser#inference_item.
    def exitInference_item(self, ctx: tptpParser.Inference_itemContext):
        pass

    # Enter a parse tree produced by tptpParser#inference_status.
    def enterInference_status(self, ctx: tptpParser.Inference_statusContext):
        pass

    # Exit a parse tree produced by tptpParser#inference_status.
    def exitInference_status(self, ctx: tptpParser.Inference_statusContext):
        pass

    # Enter a parse tree produced by tptpParser#status_value.
    def enterStatus_value(self, ctx: tptpParser.Status_valueContext):
        pass

    # Exit a parse tree produced by tptpParser#status_value.
    def exitStatus_value(self, ctx: tptpParser.Status_valueContext):
        pass

    # Enter a parse tree produced by tptpParser#inference_info.
    def enterInference_info(self, ctx: tptpParser.Inference_infoContext):
        pass

    # Exit a parse tree produced by tptpParser#inference_info.
    def exitInference_info(self, ctx: tptpParser.Inference_infoContext):
        pass

    # Enter a parse tree produced by tptpParser#assumptions_record.
    def enterAssumptions_record(self, ctx: tptpParser.Assumptions_recordContext):
        pass

    # Exit a parse tree produced by tptpParser#assumptions_record.
    def exitAssumptions_record(self, ctx: tptpParser.Assumptions_recordContext):
        pass

    # Enter a parse tree produced by tptpParser#refutation.
    def enterRefutation(self, ctx: tptpParser.RefutationContext):
        pass

    # Exit a parse tree produced by tptpParser#refutation.
    def exitRefutation(self, ctx: tptpParser.RefutationContext):
        pass

    # Enter a parse tree produced by tptpParser#new_symbol_record.
    def enterNew_symbol_record(self, ctx: tptpParser.New_symbol_recordContext):
        pass

    # Exit a parse tree produced by tptpParser#new_symbol_record.
    def exitNew_symbol_record(self, ctx: tptpParser.New_symbol_recordContext):
        pass

    # Enter a parse tree produced by tptpParser#new_symbol_list.
    def enterNew_symbol_list(self, ctx: tptpParser.New_symbol_listContext):
        pass

    # Exit a parse tree produced by tptpParser#new_symbol_list.
    def exitNew_symbol_list(self, ctx: tptpParser.New_symbol_listContext):
        pass

    # Enter a parse tree produced by tptpParser#principal_symbol.
    def enterPrincipal_symbol(self, ctx: tptpParser.Principal_symbolContext):
        pass

    # Exit a parse tree produced by tptpParser#principal_symbol.
    def exitPrincipal_symbol(self, ctx: tptpParser.Principal_symbolContext):
        pass

    # Enter a parse tree produced by tptpParser#include.
    def enterInclude(self, ctx: tptpParser.IncludeContext):
        pass

    # Exit a parse tree produced by tptpParser#include.
    def exitInclude(self, ctx: tptpParser.IncludeContext):
        pass

    # Enter a parse tree produced by tptpParser#formula_selection.
    def enterFormula_selection(self, ctx: tptpParser.Formula_selectionContext):
        pass

    # Exit a parse tree produced by tptpParser#formula_selection.
    def exitFormula_selection(self, ctx: tptpParser.Formula_selectionContext):
        pass

    # Enter a parse tree produced by tptpParser#name_list.
    def enterName_list(self, ctx: tptpParser.Name_listContext):
        pass

    # Exit a parse tree produced by tptpParser#name_list.
    def exitName_list(self, ctx: tptpParser.Name_listContext):
        pass

    # Enter a parse tree produced by tptpParser#general_term.
    def enterGeneral_term(self, ctx: tptpParser.General_termContext):
        pass

    # Exit a parse tree produced by tptpParser#general_term.
    def exitGeneral_term(self, ctx: tptpParser.General_termContext):
        pass

    # Enter a parse tree produced by tptpParser#general_data.
    def enterGeneral_data(self, ctx: tptpParser.General_dataContext):
        pass

    # Exit a parse tree produced by tptpParser#general_data.
    def exitGeneral_data(self, ctx: tptpParser.General_dataContext):
        pass

    # Enter a parse tree produced by tptpParser#general_function.
    def enterGeneral_function(self, ctx: tptpParser.General_functionContext):
        pass

    # Exit a parse tree produced by tptpParser#general_function.
    def exitGeneral_function(self, ctx: tptpParser.General_functionContext):
        pass

    # Enter a parse tree produced by tptpParser#formula_data.
    def enterFormula_data(self, ctx: tptpParser.Formula_dataContext):
        pass

    # Exit a parse tree produced by tptpParser#formula_data.
    def exitFormula_data(self, ctx: tptpParser.Formula_dataContext):
        pass

    # Enter a parse tree produced by tptpParser#general_list.
    def enterGeneral_list(self, ctx: tptpParser.General_listContext):
        pass

    # Exit a parse tree produced by tptpParser#general_list.
    def exitGeneral_list(self, ctx: tptpParser.General_listContext):
        pass

    # Enter a parse tree produced by tptpParser#general_terms.
    def enterGeneral_terms(self, ctx: tptpParser.General_termsContext):
        pass

    # Exit a parse tree produced by tptpParser#general_terms.
    def exitGeneral_terms(self, ctx: tptpParser.General_termsContext):
        pass

    # Enter a parse tree produced by tptpParser#name.
    def enterName(self, ctx: tptpParser.NameContext):
        pass

    # Exit a parse tree produced by tptpParser#name.
    def exitName(self, ctx: tptpParser.NameContext):
        pass

    # Enter a parse tree produced by tptpParser#atomic_word.
    def enterAtomic_word(self, ctx: tptpParser.Atomic_wordContext):
        pass

    # Exit a parse tree produced by tptpParser#atomic_word.
    def exitAtomic_word(self, ctx: tptpParser.Atomic_wordContext):
        pass

    # Enter a parse tree produced by tptpParser#atomic_defined_word.
    def enterAtomic_defined_word(self, ctx: tptpParser.Atomic_defined_wordContext):
        pass

    # Exit a parse tree produced by tptpParser#atomic_defined_word.
    def exitAtomic_defined_word(self, ctx: tptpParser.Atomic_defined_wordContext):
        pass

    # Enter a parse tree produced by tptpParser#atomic_system_word.
    def enterAtomic_system_word(self, ctx: tptpParser.Atomic_system_wordContext):
        pass

    # Exit a parse tree produced by tptpParser#atomic_system_word.
    def exitAtomic_system_word(self, ctx: tptpParser.Atomic_system_wordContext):
        pass

    # Enter a parse tree produced by tptpParser#number.
    def enterNumber(self, ctx: tptpParser.NumberContext):
        pass

    # Exit a parse tree produced by tptpParser#number.
    def exitNumber(self, ctx: tptpParser.NumberContext):
        pass

    # Enter a parse tree produced by tptpParser#file_name.
    def enterFile_name(self, ctx: tptpParser.File_nameContext):
        pass

    # Exit a parse tree produced by tptpParser#file_name.
    def exitFile_name(self, ctx: tptpParser.File_nameContext):
        pass
