from src.syntax.antlr_generated.tptpListener import tptpListener
from src.syntax.antlr_generated.tptpParser import tptpParser


class DimacsEncoder(tptpListener):
    def __init__(self):
        self.variables = {}
        self.number_of_variables = 0
        self.number_of_clauses = 0
        self.delimiter = 0

    @property
    def new_variable(self):
        self.number_of_variables += 1
        return self.number_of_variables

    def exitCnf_annotated(self, ctx: tptpParser.Cnf_annotatedContext):
        print('0')

    def enterCnf_literal(self, ctx: tptpParser.Cnf_literalContext):
        if ctx.getToken(tptpParser.Not, 0):
            print('-', end='')

    def enterFof_atomic_formula(self, ctx: tptpParser.Fof_atomic_formulaContext):
        atomic_formula = ctx.getText()
        variable_name = self.variables.get(atomic_formula)
        if variable_name is None:
            variable_name = self.new_variable
            self.variables[atomic_formula] = variable_name
        print(variable_name, end=' ')
