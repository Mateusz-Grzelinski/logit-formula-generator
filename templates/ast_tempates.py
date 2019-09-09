from __future__ import annotations

import itertools
import random
from abc import abstractmethod, ABC
from typing import List, Any, Iterable

from ast import *
from templates.container import *


class Template(ABC):
    @abstractmethod
    def match(self, population) -> Any:
        """:return all items from population that match template"""
        pass


class TermTemplate(Template):
    def match(self, population):
        return population


class VariableTemplate(Variable, TermTemplate):

    def __init__(self):
        super().__init__('')

    def match(self, population: List[Variable]) -> List[Variable]:
        return population


class FunctorTemplate(Functor, TermTemplate, TermTemplateContainer):
    @property
    def is_recursive(self):
        return super().is_recursive or any(
            isinstance(i, TermTemplate) or isinstance(i, FunctorTemplate) for i in self.items)

    def __init__(self, terms: List[TermTemplate, Term] = None,
                 name: str = None,
                 ):
        super().__init__(name, terms)

    @staticmethod
    def term_template_generator(arities: List[int],
                                terms: List[TermTemplate] = None
                                ):
        templates = []
        for arity in arities:
            if terms is not None:
                yield random.choices(terms, k=arity)
            else:
                yield [TermTemplate()] * arity

    def match(self, population: Iterable[Functor]) -> Iterable[Functor]:
        for functor in population:
            if len(functor.items) != len(self.items):
                continue
            for nested_template, nested_functor in zip(self.items, functor.items):
                if not nested_functor == self:
                    continue
            yield functor

    def __eq__(self, other):
        if isinstance(other, Functor):
            if len(other.items) != len(self.items):
                return False
            for nested_template, nested_functor in zip(self.items, other.items):
                if not nested_template == nested_functor:
                    return False
        return True


class Generator:
    @staticmethod
    def generate_functors(templates: List[FunctorTemplate], max_recursion_depth=0):
        functors = []
        # start generating from the least recursive structure
        templates.sort(key=lambda x: x.recursion_depth)
        assert templates[0].recursion_depth == 0  # ??

        # f(FT)
        for t in templates:
            if not t.items:
                functors.append(Functor(name=t.name, terms=[]))
                continue

            terms: List[Iterable] = []
            for nested_template in t.items:
                if isinstance(nested_template, Variable):
                    terms.append([VariableTemplate()])
                    continue
                if isinstance(nested_template, FunctorTemplate):
                    if nested_template.is_recursive:
                        print('not supp')
                    else:
                        terms.append(list(nested_template.match(functors)))

            for term_match in itertools.product(*terms):
                functors.append(Functor(name=t.name, terms=list(term_match)))
        return functors


if __name__ == '__main__':
    vt = VariableTemplate()
    ft1 = FunctorTemplate(name='f1')
    ft2 = FunctorTemplate(name='f2')
    ft3 = FunctorTemplate(name='f3',
                          terms=list(FunctorTemplate.term_template_generator(list(range(5))))
                          )
    print(ft3)
    g = Generator.generate_functors([
        ft2,
        ft3,
    ])
    print(g)

# class PredicateTemplate(Template, TermTemplateContainer):
#     def __init__(self, terms: List[TermTemplate] = None):
#         super().__init__(additional_containers=[], items=terms)
#
#     def match(self, scope) -> Any:
#         return scope.get_predicate(self)
#
#     def generate(self, name: str, variable_scope, functor_scope) -> Template:
#         # same as functor
#         pass
#
#
# class AtomTemplate(Template, TermTemplateContainer, PredicateTemplateContainer):
#
#     def __init__(self, connective: Optional[Union[str, MathOperand]],
#                  arguments: List[Union[TermTemplate, PredicateTemplate]]):
#         super().__init__(connective, arguments)
#
#
# class LiteralTemplate(Template, AtomTemplateContainer):
#     def match(self, *args, **kwargs) -> Any:
#         pass
#
#
# class CNFClauseTemplate(Template, LiteralTemplateContainer):
#     def match(self, *args, **kwargs) -> Any:
#         pass
#
#
# class CNFFormulaTemplate(Template, CNFClauseContainer):
#     def match(self, *args, **kwargs) -> Any:
#         pass
#
