from ast.containers import *


class VariableTemplateContainer(VariableContainer):
    pass


class FunctorTemplateContainer(FunctorContainer):
    @property
    def requires_functor(self):
        from templates.ast_tempates import FunctorTemplate
        return any(isinstance(t, FunctorTemplate) for t in self.items)

    @property
    def requires_variable(self):
        from templates.ast_tempates import VariableTemplate
        return any(isinstance(t, VariableTemplate) for t in self.items)


class TermTemplateContainer(VariableTemplateContainer, FunctorTemplateContainer):
    pass


class PredicateTemplateContainer(PredicateContainer):
    pass


class AtomTemplateContainer(TermTemplateContainer, PredicateTemplateContainer):
    pass


class LiteralTemplateContainer(LiteralContainer):
    pass


class CNFClauseTemplateContainer(CNFClauseContainer):
    pass
