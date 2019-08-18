from containers.atom_container import AtomContainer
from containers.variable_container import VariableContainer


class QuantifierContainer(VariableContainer, AtomContainer):
    @staticmethod
    def _type_check(obj):
        from ast.quantifier import Quantifier
        return isinstance(obj, Quantifier)
